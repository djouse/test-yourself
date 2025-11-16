# src/llm/prompts.py
PARSE_PROMPT = """
You are a reliable parser for 12th-grade Portuguese/Math exams.
Input: page text. Output: a JSON array "questions" with fields:
 - id (int), raw_text (string), type ("mcq" | "open" | "short"), choices (if mcq), topics (array), difficulty ("easy","medium","hard")
Parse question boundaries precisely, preserving numbering. Return only valid JSON.
Example output:
[{"id":1,"raw_text":"...","type":"mcq","choices":["A","B","C"],"topics":["derivatives"],"difficulty":"medium"}, ...]
----
PAGE TEXT:
{page_text}
----
Return JSON only.
"""

GENERATE_PROMPT = """
You are an exam writer. Given:
1) a list of parsed questions (as JSON),
2) retrieved IAVE criteria documents (concise bullet points),
3) options (discipline: {discipline}, grade: 12, desired_difficulty: {difficulty_profile})

Produce a new exam in JSON following this schema:
{schema_preview}

Constraints:
- Use IAVE criteria to annotate each question with competency codes and a primary skill.
- For each generated question provide: id, type, topic, difficulty, question_text, options (if mcq), answer, rationale, iave_codes.
- Keep language Portuguese for prompts & question text.
- Ensure diversity across topics and question types.
Return JSON only.
"""
