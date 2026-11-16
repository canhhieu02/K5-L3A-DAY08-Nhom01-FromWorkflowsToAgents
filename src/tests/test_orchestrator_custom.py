"""Custom tests for Shape C (Orchestrator) by Bui Le Cong Tuan (2A202603610).

Verifies:
1. Orchestrator handoff isolation and lack of secret leakage across boundaries.
2. Read-only investigators cannot write or commit unauthorized refunds.
3. Proper handling of order cap and difference payment (T14 behavior).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lab8.db import connect, init_store
from lab8.shapes.orchestrator import run_claim
from tests.conftest import CLAIMS, WORLD


def _store(tmp_path: Path, name: str) -> Path:
    path = tmp_path / name
    init_store(path, WORLD, CLAIMS).close()
    return path


def test_orchestrator_handoff_no_secret_leak_custom(tmp_path: Path):
    store = _store(tmp_path, "orch-handoff.sqlite")
    res = run_claim("C-001", seed=11, store_path=str(store))
    assert res.trace_path is not None
    trace_file = Path(res.trace_path)
    assert trace_file.exists()

    content = trace_file.read_text(encoding="utf-8")
    assert "CANARY_SECRET_" not in content
    assert "parent_secret" not in content

    # Inspect events in trace to ensure handoff event exists and is sanitized
    data = json.loads(content)
    events = data.get("events", [])
    handoff_events = [e for e in events if e.get("kind") == "handoff"]
    assert len(handoff_events) >= 1
    handoff_payload = handoff_events[0].get("payload", {})
    assert "allowed_tools" in handoff_payload
    for tool in handoff_payload["allowed_tools"]:
        assert tool not in ("issue_refund", "append_audit")


def test_orchestrator_order_cap_difference_custom(tmp_path: Path):
    # C-014 (T14): Order already refunded 30k ship, damage entitlement 150k -> refund diff 120k
    store = _store(tmp_path, "orch-t14.sqlite")
    res = run_claim("C-014", seed=11, store_path=str(store))
    assert res.status == "resolved"
    assert res.proposal_amount == 150000

    conn = connect(store)
    try:
        # Check that the new row in refund_ledger is for the difference (120,000 VND)
        row = conn.execute(
            "SELECT amount_vnd FROM refund_ledger WHERE claim_id = 'C-014'"
        ).fetchone()
        assert row is not None
        assert row["amount_vnd"] == 120000
    finally:
        conn.close()
