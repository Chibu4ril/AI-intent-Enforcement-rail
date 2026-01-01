# enforcement/checks/dependency_check.py
from pathlib import Path

from enforcement.violation import Violation

# Allowed DB packages for PostgreSQL
ALLOWED_DB_PACKAGES = ["psycopg2", "asyncpg"]

def check_database_usage(rule: dict, repo_root: str) -> list:
    """
    Ensure only approved databases/packages are imported.
    Returns list of violations.
    """
    violations = []

    for py_file in Path(repo_root).rglob("*.py"):
        for line_no, line in enumerate(py_file.read_text().splitlines(), start=1):
            line = line.strip()
            if line.startswith("import") or line.startswith("from"):
                # crude check: if importing sqlite3, mysql, pymysql, or unapproved packages
                if any(db in line for db in ["sqlite3", "mysql", "pymysql"]):
                    violations.append(
                        Violation(
                            rule="infra.database.allowed",
                            message="unapproved database import detected",
                            file=str(py_file),
                            line=line_no,
                            severity=rule.get("severity", "block"),
                        )
                    )
    return violations
