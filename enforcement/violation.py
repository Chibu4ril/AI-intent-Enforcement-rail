from dataclasses import dataclass
from typing import Optional

@dataclass
class Violation:
    def __init__(self, rule: str, message: str, file: str, line: int, suggestion: str = None, severity: str = "block", auto_fix_applied: bool = False):
        self.rule = rule
        self.message = message
        self.file = file
        self.line = line
        self.suggestion = suggestion
        self.severity = severity
        self.auto_fix_applied = auto_fix_applied

    def to_dict(self):
        return {
            "rule": self.rule,
            "message": self.message,
            "file": self.file,
            "line": self.line,
            "suggestion": self.suggestion,
            "severity": self.severity,
            "auto_fix_applied": self.auto_fix_applied
        }
