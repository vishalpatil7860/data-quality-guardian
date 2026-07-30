from __future__ import annotations
from dqguardian.checks.base import BaseCheck, CheckResult

class UniquenessCheck(BaseCheck):
    type = "uniqueness"
    def run(self) -> CheckResult:
        if not self.table:
            return self._error("No table specified")
        if not self.columns:
            return self._error("No columns specified")
        try:
            total = self.db.get_row_count(self.table)
            if total == 0:
                return self._pass(1.0, 0, "Table is empty")
            cols = ", ".join(f'"{c}"' for c in self.columns)
            sql = f"SELECT COUNT(*) FROM (SELECT {cols} FROM {self.table} GROUP BY {cols} HAVING COUNT(*) > 1) AS dupes"
            duplicate_groups = self.db.execute_scalar(sql) or 0
            sql2 = f"SELECT COALESCE(SUM(cnt), 0) FROM (SELECT COUNT(*) AS cnt FROM {self.table} GROUP BY {cols} HAVING COUNT(*) > 1) AS dupes"
            duplicate_rows = self.db.execute_scalar(sql2) or 0
            unique_pct = 1.0 - (duplicate_rows / total)
            score = max(unique_pct, 0.0)
            details = {"total_rows": total, "duplicate_rows": duplicate_rows, "duplicate_groups": duplicate_groups, "unique_pct": round(unique_pct * 100, 2)}
            if score >= self.threshold:
                return self._pass(score, details, f"Unique {round(score * 100, 2)}% - {duplicate_rows} duplicate rows")
            return self._fail(score, details, f"Unique {round(score * 100, 2)}% below threshold {round(self.threshold * 100, 0)}%")
        except Exception as e:
            return self._error(f"Uniqueness check failed: {e}")