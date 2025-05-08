import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

class VectorStore:
    def __init__(self, embedding_model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embedding_model_name)
        self.index = faiss.IndexFlatL2(self.model.get_sentence_embedding_dimension())
        self.documents = []
        self.embeddings = []

    def build_index(self, texts: list):
        self.documents = texts
        self.embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        self.index.add(self.embeddings)

    def query(self, text: str, top_k=5):
        query_embedding = self.model.encode([text], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.documents[i] for i in indices[0]]
