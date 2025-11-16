import json
from src.llm.local_model import LocalLlama
from src.llm.prompts import PARSE_PROMPT

def parse_page(page_text: str, llm: LocalLlama):
    prompt = PARSE_PROMPT.format(page_text=page_text)
    resp = llm.generate(prompt, max_tokens=1024)
    try:
        parsed = json.loads(resp)
    except Exception as e:
        # fallback: try to extract JSON substring
        import re
        m = re.search(r"\[.*\]", resp, re.S)
        parsed = json.loads(m.group(0)) if m else []
    return parsed
