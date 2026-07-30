from __future__ import annotations
import json
from datetime import datetime
from typing import Any, Dict, List
from dqguardian.checks.base import CheckResult

def to_json(results: List[CheckResult], indent: int = 2) -> str:
    data = _build_report(results)
    return json.dumps(data, indent=indent, default=str)

def _build_report(results: List[CheckResult]) -> Dict[str, Any]:
    total = len(results)
    passed = sum(1 for r in results if r.status == "pass")
    failed = sum(1 for r in results if r.status == "fail")
    errors = sum(1 for r in results if r.status == "error")
    return {
        "run_id": datetime.utcnow().isoformat(),
        "summary": {"total": total, "passed": passed, "failed": failed, "errors": errors, "pass_rate": round(passed / total, 4) if total > 0 else 0.0},
        "checks": [{"name": r.name, "type": r.check_type, "status": r.status, "score": r.score, "threshold": r.threshold, "actual_value": r.actual_value, "message": r.message, "table": r.table, "duration_ms": r.duration_ms, "timestamp": r.timestamp.isoformat()} for r in results],
    }