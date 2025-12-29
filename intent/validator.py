
REQUIRED_SECTIONS = {"project", "security"}

class IntentValidator:
    def __init__(self, intent: dict):
        self.intent = intent

    def validate(self) -> None:
        self._validate_required_sections()
        self._validate_security()
        self._validate_infra()

    def _validate_required_sections(self):
        missing = REQUIRED_SECTIONS - self.intent.keys()
        if missing:
            raise ValueError(f"Missing required intent sections: {missing}")

    def _validate_security(self):
        security = self.intent.get("security", {})
        if "require_auth" in security:
            if not isinstance(security["require_auth"], bool):
                raise ValueError("security.require_auth must be boolean")

        if "forbid_secret_logging" in security:
            if not isinstance(security["forbid_secret_logging"], bool):
                raise ValueError("security.forbid_secret_logging must be boolean")

    def _validate_infra(self):
        infra = self.intent.get("infra")
        if not infra:
            return

        allowed_dbs = infra.get("allowed_databases")
        if allowed_dbs is not None:
            if not isinstance(allowed_dbs, list) or not all(isinstance(db, str) for db in allowed_dbs):
                raise ValueError("infra.allowed_databases must be a list of strings")
