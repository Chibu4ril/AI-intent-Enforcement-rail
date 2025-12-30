# enforcement/types.py
from dataclasses import dataclass

@dataclass
class Violation:
    file: str
    line: int
    rule: str
    message: str
    severity: str = "block"
    suggestion: str | None = None
    auto_fixable: bool = False
    auto_fix_applied: bool = False
