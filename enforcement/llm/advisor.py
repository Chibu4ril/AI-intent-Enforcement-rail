from enforcement.types import Violation
from enforcement.llm.prompts import build_prompt
import os
from huggingface_hub import InferenceClient
import re

client = InferenceClient(
    model="meta-llama/Llama-2-7b-chat-hf",
    token=os.getenv("HF_TOKEN"),
    timeout=30,
)

def enrich_violation(v: Violation, code_snippet: str) -> Violation:
    if not v.code_snippet:
        return v
    
    prompt = build_prompt(v, code_snippet)

    try:
        response = client.text_generation(
            prompt,
            max_new_tokens=200,
            temperature=0.4,   # lower = safer code
            top_p=0.9,
            stop_sequences=["</s>"],
        )
        v.suggestion = extract_suggestion(response)

    except Exception as e:
        v.suggestion = f"# LLM suggestion unavailable: {str(e)}"

    return v


def extract_suggestion(llm_content: str) -> str:
    """
    Extract suggested code snippet from LLM output.
    """
    match = re.search(r"```(?:python)?\n(.*?)```", llm_content, re.DOTALL)
    if match:
        return match.group(1).strip()

    return llm_content.strip()
