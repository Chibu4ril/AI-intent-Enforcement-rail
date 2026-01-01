# enforcement/violation.py
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
