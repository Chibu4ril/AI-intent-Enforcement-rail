# enforcement/llm/prompts.py
def build_prompt(v, code):
    return f"""
You are a senior backend security engineer.

Violation:
Rule: {v.rule}
Message: {v.message}
File: {v.file}
Line: {v.line}

Code:
```python
{code}
"""