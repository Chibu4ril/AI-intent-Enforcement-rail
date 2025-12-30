from compiler.registry import RULE_REGISTRY

def compile_policies(normalized_policies: dict) -> dict:
    compiled_checks = []

    for policy_key, policy_value in normalized_policies.items():
        compiler_fn = RULE_REGISTRY.get(policy_key)

        if not compiler_fn:
            continue  # unsupported policy (for now)

        checks = compiler_fn(policy_value)
        compiled_checks.extend(checks)

    return {
        "checks": compiled_checks
    }
