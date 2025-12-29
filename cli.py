import json
import sys
from intent.parser import IntentParser
from intent.validator import IntentValidator
from intent.normalizer import IntentNormalizer

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

if __name__ == "__main__":
    try:
        compile_intent()
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
