import ast
from pathlib import Path
from enforcement.violation import Violation



def check_auth(rule: dict, repo_root: str) -> list:
    """
    Enforces: security.auth.required
    """
    violations = []
    rule_id = rule.get("id", "security.auth.required")

    for py_file in Path(repo_root).rglob("*.py"):
        source = py_file.read_text()
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if is_fastapi_route(node) and not has_auth_dependency(node):
                violations.append(Violation(
                        rule=rule_id,
                        message="Route missing authentication dependency",
                        file=str(py_file),
                        line=node.lineno,
                        suggestion="@router.get(..., dependencies=[Depends(get_current_user)])"
                    ))

    return violations



def is_fastapi_route(node):
    if not isinstance(node, ast.FunctionDef):
        return False

    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call):
            if hasattr(decorator.func, "attr"):
                if decorator.func.attr in {"get", "post", "put", "delete", "patch"}:
                    return True
    return False

def has_auth_dependency(node: ast.FunctionDef) -> bool:
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call):
            continue

        for keyword in decorator.keywords:
            if keyword.arg != "dependencies":
                continue

            if isinstance(keyword.value, ast.List):
                for elt in keyword.value.elts:
                    if is_auth_depends_call(elt):
                        return True

    return False


# Configurable 

def is_auth_depends_call(node):
    if not isinstance(node, ast.Call):
        return False

    if isinstance(node.func, ast.Name) and node.func.id == "Depends":
        if node.args:
            arg = node.args[0]
            if isinstance(arg, ast.Name):
                return arg.id in {
                    "get_current_user",
                    "get_current_active_user",
                    "require_auth"
                }
    return False
