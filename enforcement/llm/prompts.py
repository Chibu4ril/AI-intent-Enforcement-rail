def build_prompt(v, code):
    return f"""<s>[INST]
You are a senior backend security engineer.
Your task is to suggest a minimal, correct code fix.
Do NOT explain. Return only the corrected code.

Violation:
Rule: {v.rule}
Message: {v.message}
File: {v.file}
Line: {v.line}

Code:
```python
{code}

```</s>[/INST]"""