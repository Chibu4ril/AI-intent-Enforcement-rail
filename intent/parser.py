
import yaml
from pathlib import Path

class IntentParser:
    def __init__(self, intent_path: str):
        self.intent_path = Path(intent_path)

    def load(self) -> dict:
        if not self.intent_path.exists():
            raise FileNotFoundError(f"Intent file not found: {self.intent_path}")

        with open(self.intent_path, "r") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            raise ValueError("Intent file must be a YAML mapping")

        return data
