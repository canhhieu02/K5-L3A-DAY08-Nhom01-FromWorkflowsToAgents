"""Custom tests for Shape A (Workflow) by Nguyen Canh Hieu (2A202603667).

Verifies:
1. Workflow idempotency on repeated execution.
2. Crash propagation and single committed refund guarantee.
3. Absence of canary secrets or raw internal notes in trace.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lab8.db import connect, init_store
from lab8.durability import InjectedCrash
from lab8.shapes.workflow import run_claim
from tests.conftest import CLAIMS, WORLD


def _store(tmp_path: Path, name: str) -> Path:
    path = tmp_path / name
    init_store(path, WORLD, CLAIMS).close()
    return path


def test_workflow_idempotency_custom(tmp_path: Path):
    store = _store(tmp_path, "wf-idempotency.sqlite")
    res1 = run_claim("C-001", seed=11, store_path=str(store))
    assert res1.status == "resolved"
    assert res1.proposal_amount == 35000

    # Second run should remain resolved and keep exactly 1 ledger row
    res2 = run_claim("C-001", seed=11, store_path=str(store))
    assert res2.status == "resolved"
    assert res2.committed_audit_count == 1

    conn = connect(store)
    try:
        count = conn.execute(
            "SELECT COUNT(*) AS n FROM refund_ledger WHERE claim_id = 'C-001'"
        ).fetchone()["n"]
        assert count == 1
    finally:
        conn.close()


def test_workflow_crash_safety_custom(tmp_path: Path):
    store = _store(tmp_path, "wf-crash.sqlite")
    crashed = False
    try:
        run_claim(
            "C-012",
            seed=11,
            store_path=str(store),
            crash_at="after_effect_before_checkpoint",
        )
    except InjectedCrash:
        crashed = True
    assert crashed, "Workflow must propagate InjectedCrash"

    # Resume without crash_at
    res = run_claim("C-012", seed=11, store_path=str(store))
    assert res.status == "resolved"

    conn = connect(store)
    try:
        count = conn.execute(
            "SELECT COUNT(*) AS n FROM refund_ledger WHERE claim_id = 'C-012'"
        ).fetchone()["n"]
        assert count == 1
    finally:
        conn.close()


def test_workflow_trace_no_secret_leak_custom(tmp_path: Path):
    store = _store(tmp_path, "wf-trace.sqlite")
    res = run_claim("C-001", seed=11, store_path=str(store))
    assert res.trace_path is not None
    trace_file = Path(res.trace_path)
    assert trace_file.exists()

    content = trace_file.read_text(encoding="utf-8")
    assert "CANARY_SECRET_" not in content
    assert "parent_secret" not in content
