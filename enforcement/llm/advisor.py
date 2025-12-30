# enforcement/llm/advisor.py
from enforcement.types import Violation
from enforcement.llm.prompts import build_prompt
import os
from openai import OpenAI
import re


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def enrich_violation(v: Violation, code_snippet: str) -> Violation:
    prompt = build_prompt(v, code_snippet)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    content = response.choices[0].message.content

    v.suggestion = extract_suggestion(content)
    return v

def extract_suggestion(llm_content: str) -> str:
    """
    Extract suggested code snippet from LLM output.
    """
    # If LLM returns triple-backtick blocks, extract them
    match = re.search(r"```(?:python)?\n(.*?)```", llm_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return llm_content.strip()
