import sqlite3
from typing import List, Dict, Any

class CheckEngine:
    def __init__(self, db_path: str = "dq_results.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS check_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                check_name TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL,
                details TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def register_check(self, check_name: str, check_function):
        # This would ideally interact with a CheckRegistry,
        # but for this example, we''ll keep it simple.
        # Assume a global or passed-in registry if this were a larger system.
        print(f"Registering check: {check_name}")
        pass

    def run_checks(self, database_connection_string: str, checks_to_run: List[Dict[str, Any]]):
        results = []
        # Simulate database connection
        print(f"Connecting to database: {database_connection_string}")

        for check_info in checks_to_run:
            check_name = check_info.get("name")
            check_query = check_info.get("query")
            expected_value = check_info.get("expected_value")

            status = "PASS"
            details = "Check executed successfully."

            try:
                # Simulate executing query against database
                # In a real scenario, this would use the database_connection_string
                # to connect and execute the check_query.
                # For now, we''ll just simulate a result.
                actual_value = 10 # Simulate a query result
                if check_query and expected_value is not None:
                    if actual_value != expected_value:
                        status = "FAIL"
                        details = f"Expected {expected_value}, got {actual_value}"
                elif check_query:
                    # If no expected_value, just record query execution
                    details = f"Query executed, result: {actual_value}"


            except Exception as e:
                status = "ERROR"
                details = f"Error during check execution: {e}"

            self._persist_result(check_name, status, details)
            results.append({
                "check_name": check_name,
                "status": status,
                "details": details
            })
        return results

    def _persist_result(self, check_name: str, status: str, details: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO check_results (check_name, status, details) VALUES (?, ?, ?)",
            (check_name, status, details)
        )
        conn.commit()
        conn.close()
        print(f"Persisted result for {check_name}: {status}")

    def get_all_results(self) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT check_name, timestamp, status, details FROM check_results ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()
        results = []
        for row in rows:
            results.append({
                "check_name": row[0],
                "timestamp": row[1],
                "status": row[2],
                "details": row[3]
            })
        return results
