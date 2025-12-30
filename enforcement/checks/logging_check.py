import ast
from pathlib import Path

def check_logging(rule: dict, repo_root: str) -> list:
    """
    Detect logging of secrets or print statements containing sensitive info.
    Returns a list of violations.
    """
    violations = []

    for py_file in Path(repo_root).rglob("*.py"):
        source = py_file.read_text()
        tree = ast.parse(source, filename=str(py_file))

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # detect print(...)
                if getattr(node.func, "id", "") == "print":
                    violations.append({
                        "file": str(py_file),
                        "line": node.lineno,
                        "message": "print statement detected (possible secret leak)"
                    })
                # detect logger.info(...), logger.warning(...), etc.
                elif hasattr(node.func, "attr") and node.func.attr in ("info", "warning", "error", "debug"):
                    violations.append({
                        "file": str(py_file),
                        "line": node.lineno,
                        "message": f"logging call detected: {node.func.attr} (possible secret leak)"
                    })

    return violations
