from dataclasses import dataclass
from typing import Optional

@dataclass
class Violation:
    rule: str
    message: str
    file: str
    line: int
    severity: str
    code_snippet: Optional[str] = None
    suggestion: Optional[str] = None

    def to_dict(self):
        return {
            "rule": self.rule,
            "message": self.message,
            "file": self.file,
            "line": self.line,
            "severity": self.severity,
            "code_snippet": self.code_snippet,
            "suggestion": self.suggestion,
        }
