# src/main.py
import json
from src.tools.pdf_extract import extract_pdf_text
from src.tools.parse_questions import parse_page
from src.rag.indexer import create_document_store
from src.rag.retriever import RagRetriever
from src.tools.generator import generate_exam
from src.llm.local_model import LocalLlama

def run_pipeline(pdf_path, model_path, iave_index_path="faiss_index", iave_docs_dir="data/iave"):
    # 1. Extract pages
    pages = extract_pdf_text(pdf_path)
    # 2. LLM init
    llm = LocalLlama(model_path)
    # 3. Index / load IAVE doc store
    store = create_document_store(index_path=iave_index_path)
    # If store empty, call index_documents(...) once to load IAVE docs
    retriever = RagRetriever(store)
    # 4. Parse pages -> accumulate questions
    all_parsed = []
    for p in pages:
        parsed = parse_page(p["text"], llm)
        all_parsed.extend(parsed)
    # 5. Retrieve IAVE docs relevant to whole exam
    combined_text = " ".join([q.get("raw_text","") for q in all_parsed])
    retrieved = retriever.retrieve(combined_text, top_k=8)
    # 6. Generate new exam JSON
    options = {"discipline":"Mathematics", "grade":12, "difficulty":"mixed", "schema": {}}
    exam = generate_exam(all_parsed, retrieved, options, llm)
    print(json.dumps(exam, ensure_ascii=False, indent=2))
    return exam

if __name__ == "__main__":
    import sys
    pdf = sys.argv[1]
    model = sys.argv[2]
    run_pipeline(pdf, model)
