from typing import Dict

class IntentNormalizer:
    def __init__(self, intent: dict):
        self.intent = intent

    def normalize(self) -> Dict[str, dict]:
        rules = {}

        security = self.intent.get("security", {})
        infra = self.intent.get("infra", {})

        # ---- Security Rules ----
        if security.get("require_auth") is True:
            rules["security.auth.required"] = {
                "value": True,
                "severity": "block",
                "scope": "code",
                "description": "All public routes must require authentication"
            }

        if security.get("forbid_secret_logging") is True:
            rules["logging.secrets.allowed"] = {
                "value": False,
                "severity": "block",
                "scope": "code",
                "description": "Secrets must not be logged"
            }

        # ---- Infra Rules ----
        allowed_dbs = infra.get("allowed_databases")
        if allowed_dbs:
            rules["infra.database.allowed"] = {
                "value": allowed_dbs,
                "severity": "block",
                "scope": "infra",
                "description": "Only approved databases may be used"
            }

        if not rules:
            raise ValueError("No enforceable rules could be derived from intent")

        return rules