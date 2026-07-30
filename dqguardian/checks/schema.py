from __future__ import annotations
from dqguardian.checks.base import BaseCheck, CheckResult

class SchemaDriftCheck(BaseCheck):
    type = "schema"
    def run(self) -> CheckResult:
        if not self.table:
            return self._error("No table specified")
        expected_columns = self.config.get("columns", [])
        expected_types = self.config.get("column_types", {})
        try:
            actual_columns = self.db.get_columns(self.table)
            actual_names = {c["name"] for c in actual_columns}
            actual_types = {c["name"]: c["type"] for c in actual_columns}
            issues = []
            if expected_columns:
                missing = [c for c in expected_columns if c not in actual_names]
                if missing:
                    issues.append(f"Missing columns: {missing}")
                unexpected = [c for c in actual_names if c not in expected_columns]
                if unexpected:
                    issues.append(f"Unexpected columns: {unexpected}")
            if expected_types:
                for col, expected_type in expected_types.items():
                    actual_type = actual_types.get(col)
                    if actual_type and expected_type.lower() not in actual_type.lower():
                        issues.append(f"Type mismatch: {col} expected {expected_type}, got {actual_type}")
            if not issues:
                n_cols = len(actual_columns)
                return self._pass(1.0, {"column_count": n_cols, "columns": [c["name"] for c in actual_columns]}, f"Schema OK: {n_cols} columns match expectation")
            issue_count = len(issues)
            score = max(0.0, 1.0 - (issue_count / max(len(actual_columns), 1)))
            return self._fail(score, {"issues": issues, "actual_columns": [c["name"] for c in actual_columns]}, f"Schema drift detected: {"; ".join(issues)}")
        except Exception as e:
            return self._error(f"Schema check failed: {e}")