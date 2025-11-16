from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack import Document
import os
import glob

def create_document_store():
    store = InMemoryDocumentStore()
    return store

def index_documents(store: InMemoryDocumentStore, files_dir: str, embedding_model_name="all-MiniLM-L6-v2"):
    embedder = SentenceTransformersDocumentEmbedder(model=embedding_model_name)
    docs = []
    for path in glob.glob(os.path.join(files_dir, "**/*.*"), recursive=True):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        meta = {"source": os.path.basename(path), "path": path}
        docs.append(Document(content=text, meta=meta))
    
    embedded_docs = embedder.run(docs)["documents"]
    store.write_documents(embedded_docs)
    return store