from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.document_stores.in_memory import InMemoryDocumentStore

class RagRetriever:
    def __init__(self, store: InMemoryDocumentStore, model_name="all-MiniLM-L6-v2"):
        self.store = store
        self.text_embedder = SentenceTransformersTextEmbedder(model=model_name)
        self.retriever = InMemoryEmbeddingRetriever(document_store=store)
    
    def retrieve(self, query: str, top_k=5):
        query_embedding = self.text_embedder.run(text=query)["embedding"]
        hits = self.retriever.run(query_embedding=query_embedding, top_k=top_k)["documents"]
        return hits 
