from compiler.rules import compile_security_auth_required

RULE_REGISTRY = {
    "security.auth.required": compile_security_auth_required
}
