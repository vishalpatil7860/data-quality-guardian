from __future__ import annotations
from dqguardian.checks.base import BaseCheck, CheckResult

class CustomSQLCheck(BaseCheck):
    type = "custom_sql"
    def run(self) -> CheckResult:
        query = self.config.get("query")
        if not query:
            return self._error("No query specified")
        max_value = self.config.get("max_value")
        min_value = self.config.get("min_value")
        expected_value = self.config.get("expected_value")
        try:
            result = self.db.execute_scalar(query)
            if expected_value is not None:
                if result == expected_value:
                    return self._pass(1.0, result, f"Result {result} matches expected {expected_value}")
                return self._fail(0.0, result, f"Result {result} does not match expected {expected_value}")
            if min_value is not None and max_value is not None:
                if min_value <= result <= max_value:
                    range_size = max_value - min_value
                    score = 1.0 if range_size == 0 else max(0.0, min(1.0, 1.0 - abs(result - (min_value + max_value) / 2) / (range_size / 2)))
                    return self._pass(score, result, f"Result {result} in range [{min_value}, {max_value}]")
                return self._fail(0.0, result, f"Result {result} outside range [{min_value}, {max_value}]")
            if max_value is not None:
                if result <= max_value:
                    return self._pass(1.0, result, f"Result {result} <= max {max_value}")
                return self._fail(0.0, result, f"Result {result} exceeds max {max_value}")
            if min_value is not None:
                if result >= min_value:
                    return self._pass(1.0, result, f"Result {result} >= min {min_value}")
                return self._fail(0.0, result, f"Result {result} below min {min_value}")
            return self._pass(1.0, result, f"Result: {result}")
        except Exception as e:
            return self._error(f"Custom SQL check failed: {e}")