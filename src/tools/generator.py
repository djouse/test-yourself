# src/tools/generator.py
import json
from src.llm.local_model import LocalLlama
from src.llm.prompts import GENERATE_PROMPT

def generate_exam(parsed_questions, retrieved_iave_docs, options, llm: LocalLlama):
    iave_text = "\n\n".join([d.content for d in retrieved_iave_docs])
    schema_preview = json.dumps(options['schema'], indent=2)
    prompt = GENERATE_PROMPT.format(
        discipline=options['discipline'],
        difficulty_profile=options.get("difficulty", "mixed"),
        schema_preview=schema_preview
    )
    # Append JSON inputs in a concise form
    prompt += "\n\nPARSED_QUESTIONS:\n" + json.dumps(parsed_questions, ensure_ascii=False)[:8000]
    prompt += "\n\nIAVE_DOCS:\n" + iave_text[:8000]
    resp = llm.generate(prompt, max_tokens=1500, temperature=0.2)
    # Expect JSON only
    try:
        exam_json = json.loads(resp)
    except:
        import re
        m = re.search(r"\{.*\}", resp, re.S)
        exam_json = json.loads(m.group(0)) if m else {}
    return exam_json
