import argparse
import sys
import json
from intent.parser import IntentParser
from intent.validator import IntentValidator
from intent.normalizer import IntentNormalizer
from enforcement.ci_gate import enforce
from enforcement.violation import Violation


INTENT_FILE = "intent/intent.yaml"
LOCK_FILE = "intent/intent.lock.json"

def compile_intent():
    parser = IntentParser(INTENT_FILE)
    intent = parser.load()

    validator = IntentValidator(intent)
    validator.validate()

    normalizer = IntentNormalizer(intent)
    rules = normalizer.normalize()

    with open(LOCK_FILE, "w") as f:
        json.dump(rules, f, indent=2)

    print(f"[OK] Intent compiled successfully → {LOCK_FILE}")


def assert_valid_violations(violations):
    for v in violations:
        if not isinstance(v, Violation):
            raise TypeError(
                f"Invalid violation emitted: {type(v)} — expected Violation"
            )


def main():
    parser = argparse.ArgumentParser(description="Intent CLI")
    parser.add_argument(
        "action",
        choices=["compile", "enforce"],
        help="compile → parse/validate/normalize intent, enforce → run CI checks",
    )
    args = parser.parse_args()

    try:
        if args.action == "compile":
            compile_intent()
        elif args.action == "enforce":
            enforce()
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
