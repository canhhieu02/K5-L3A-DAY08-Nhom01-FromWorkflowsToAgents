"""Shape B — one ReAct agent. Student work.

Signature (do not change):

    run_claim(claim_id, *, seed, store_path, crash_at=None) -> RunResult
"""

from __future__ import annotations

import sqlite3
from typing import Any

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.mock_llm import complete
from lab8.runtime import run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish
from lab8.tools import get_claim_view, tool_cost
from lab8.trace import Trace


class _Trace:
    """Local wrapper so a crash can still flush trace before re-raising."""

    def __init__(self, run_id: str) -> None:
        self._inner = Trace(run_id)

    def add(self, kind: str, payload: dict) -> None:
        self._inner.add(kind, payload)

    def write(self) -> str:
        return self._inner.write()

    @property
    def run_id(self) -> str:
        return self._inner.run_id


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def _run(
    conn: sqlite3.Connection,
    claim_id: str,
    *,
    seed: int,
    crash_at: str | None,
) -> RunResult:
    budget = Budget()
    run_id = make_run_id("single", claim_id, seed)
    trace = _Trace(run_id)

    # 1. Read claim view
    budget.add_tool(tool_cost())
    claim_view = get_claim_view(conn, claim_id)
    if not claim_view.get("found"):
        trace.add("error", {"reason": "unknown_claim"})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="failed",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason="unknown_claim",
        )

    trace.add("claim", {"claim_id": claim_id, "order_id": claim_view.get("order_id")})

    # Missing order_id -> early finish
    if not claim_view.get("order_id"):
        complete(budget, seed=seed, purpose="draft", prompt="needs_info")
        trace.add("decision", {"status": "needs_info"})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="needs_info",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason="missing_order_id",
        )

    # ReAct agent loop
    # Decide policy:
    # Step 1: lookup_order
    # Step 2: if visible -> compute_compensation
    # Step 3: finalize with quote
    def decide(seen: dict[str, Any]) -> dict[str, Any]:
        complete(budget, seed=seed, purpose="decide", prompt=str(seen.get("last_tool")))
        last_tool = seen.get("last_tool")
        if last_tool is None:
            return {
                "tool": "lookup_order",
                "args": {
                    "order_id": claim_view.get("order_id"),
                    "principal_id": claim_view.get("principal_id"),
                },
            }

        if last_tool == "lookup_order":
            order_view = seen.get("last_result") or {}
            if not order_view.get("visible"):
                return {
                    "final": {
                        "status": "escalated",
                        "reason": order_view.get("reason"),
                        "proposal": 0,
                    }
                }
            return {
                "tool": "compute_compensation",
                "args": {"order": order_view["order"]},
            }

        if last_tool == "compute_compensation":
            quote_payload = seen.get("last_result") or {}
            amount = int(quote_payload.get("amount_vnd", 0))
            return {
                "final": {
                    "status": "quote_ready",
                    "proposal": amount,
                    "quote_payload": quote_payload,
                    "reason": quote_payload.get("reason"),
                }
            }

        return {"final": {"status": "failed", "error_reason": "unexpected_step"}}

    react_result = run_react(
        conn,
        budget,
        observation={"claim": claim_view},
        decide=decide,
        max_steps=8,
        worker=False,
    )
    trace.add("react", {"stopped": react_result.get("stopped")})

    final = react_result.get("final") or {}
    final_status = final.get("status")

    if react_result.get("stopped") == "step_cap" or final_status == "failed":
        trace.add("decision", {"status": "failed"})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="failed",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=final.get("error_reason", "step_cap"),
        )

    if final_status == "escalated":
        complete(budget, seed=seed, purpose="draft", prompt="escalated")
        trace.add("decision", {"status": "escalated"})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="escalated",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=final.get("reason"),
        )

    proposal = int(final.get("proposal", 0))
    trace.add("quote", final.get("quote_payload", {"amount_vnd": proposal}))
    complete(budget, seed=seed, purpose="draft", prompt=f"proposal={proposal}")

    if proposal <= 0:
        trace.add("decision", {"status": "denied"})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="denied",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=final.get("reason"),
        )

    # Quote > 0: durability.issue_refund with FULL quote and crash_at
    try:
        outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
    except InjectedCrash:
        trace.add("crash", {"at": crash_at})
        trace.write()
        raise

    if not outcome["ok"]:
        status = "failed" if outcome.get("conflict") else "denied"
        trace.add("decision", {"status": status, "reason": outcome.get("reason")})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status=status,
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=outcome.get("reason"),
        )

    trace.add("decision", {"status": "resolved"})
    return finish(
        conn,
        shape="single",
        claim_id=claim_id,
        seed=seed,
        status="resolved",
        proposal_amount=proposal,
        budget=budget,
        trace=trace,
        error_reason=None,
    )
