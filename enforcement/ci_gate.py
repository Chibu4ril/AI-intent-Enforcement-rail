import json
import sys
import glob
from pathlib import Path
from enforcement.checks import auth_check, logging_check, dependency_check
from enforcement.llm.advisor import enrich_violation



LOCK_FILE = "intent/intent.lock.json"
REPO_ROOT = "."  # root of the repo to scan
CONTEXT_LINES = 5  # Number of lines before/after violation line

def attach_code_snippets(violations):
    """
    For each violation, attach the surrounding code snippet for LLM context.
    """
    for v in violations:
        file_path = Path(v["file"])
        if not file_path.exists():
            v["code_snippet"] = "<file not found>"
            continue

        lines = file_path.read_text().splitlines()
        line_idx = v["line"] - 1  # convert 1-based to 0-based index

        start = max(line_idx - CONTEXT_LINES, 0)
        end = min(line_idx + CONTEXT_LINES + 1, len(lines))

        snippet = "\n".join(lines[start:end])
        v["code_snippet"] = snippet

    return violations



def enforce():
    with open(LOCK_FILE) as f:
        rules = json.load(f)

    violations = []

    # Auth enforcement
    auth_rule = rules.get("security.auth.required", {})
    if auth_rule.get("value"):
        violations += auth_check.check_auth(auth_rule, REPO_ROOT)

    # Logging enforcement
    logging_rule = rules.get("logging.secrets.allowed", {})
    if not logging_rule.get("value"):
        violations += logging_check.check_logging(logging_rule, REPO_ROOT)

    # Database enforcement
    db_rule = rules.get("infra.database.allowed", {})
    if db_rule.get("value"):
        violations += dependency_check.check_database_usage(db_rule, REPO_ROOT)
        
    # code snippets ---
    violations = attach_code_snippets(violations)


    # --- Enrich violations with LLM suggestions ---
    enriched_violations = []
    for v in violations:
        code_snippet = v.get("code_snippet", "")
        enriched_v = enrich_violation(v, code_snippet)
        enriched_violations.append(enriched_v)

    # Print enriched violations
    if enriched_violations:
        print("[FAIL] Policy violations detected with suggestions:")
        for v in enriched_violations:
            v_dict = v.to_dict() if hasattr(v, "to_dict") else v
            print(f" - {v_dict['file']}:{v_dict['line']} → {v_dict['message']}")
            print(f"   Suggestion: {v_dict.get('suggestion', 'No suggestion')}")
        sys.exit(1)
    else:
        print("[PASS] No policy violations detected.")


if __name__ == "__main__":
    enforce()
