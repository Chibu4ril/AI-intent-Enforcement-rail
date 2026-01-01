import json
import sys
from pathlib import Path
from enforcement.checks import auth_check, logging_check, dependency_check
from enforcement.llm.advisor import enrich_violation
from enforcement.violation import Violation



LOCK_FILE = "intent/intent.lock.json"
REPO_ROOT = "."  
CONTEXT_LINES = 5 

def attach_code_snippets(violations: list[Violation]) -> list[Violation]:
    for v in violations:
        file_path = Path(v.file)

        if not file_path.exists():
            v.code_snippet = "<file not found>"
            continue

        lines = file_path.read_text().splitlines()
        idx = v.line - 1

        start = max(idx - CONTEXT_LINES, 0)
        end = min(idx + CONTEXT_LINES + 1, len(lines))

        v.code_snippet = "\n".join(lines[start:end])

    return violations


def enrich_violations_with_llm(violations):
    enriched = []

    for v in violations:
        if not hasattr(v, "code_snippet"):
            enriched.append(v)
            continue

        try:
            v = enrich_violation(v, v.code_snippet)
        except Exception as e:
            v.suggestion = f"LLM enrichment failed: {str(e)}"

        enriched.append(v)

    return enriched


def enforce():
    with open(LOCK_FILE) as f:
        rules = json.load(f)

    violations: list[Violation] = []

    # 1️⃣ Collect violations (STRICTLY Violation objects)
    auth_rule = rules.get("security.auth.required", {})
    if auth_rule.get("value"):
        violations.extend(auth_check.check_auth(auth_rule, REPO_ROOT))

    logging_rule = rules.get("logging.secrets.allowed", {})
    if not logging_rule.get("value"):
        violations.extend(logging_check.check_logging(logging_rule, REPO_ROOT))

    db_rule = rules.get("infra.database.allowed", {})
    if db_rule.get("value"):
        violations.extend(dependency_check.check_database_usage(db_rule, REPO_ROOT))

    if not violations:
        print("[PASS] No policy violations detected.")
        return

    violations = attach_code_snippets(violations)

    violations = enrich_violations_with_llm(violations)

    print("[FAIL] Policy violations detected with suggestions:\n")
    for v in violations:
        print(f"File: {v.file}:{v.line}")
        print(f"Rule: {v.rule}")
        print(f"Issue: {v.message}")
        if v.suggestion:
            print("Suggested fix:")
            print(v.suggestion)
        print("-" * 60)

    sys.exit(1)


if __name__ == "__main__":
    enforce()
