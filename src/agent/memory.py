from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime

import faiss
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

@dataclass
class IncidentDocument:
    id: str
    content: str
    source: str  # 'slack' or 'confluence'
    url: str
    timestamp: datetime
    embedding: List[float] = None

class VectorMemory:
    def __init__(self, embedding_model: Embeddings = None):
        self.embedding_model = embedding_model or OpenAIEmbeddings()
        self.dimension = 1536  # OpenAI embedding dimension
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents: List[IncidentDocument] = []
    
    def add_document(self, document: IncidentDocument):
        """Add a document to the vector store"""
        if not document.embedding:
            document.embedding = self.embedding_model.embed_query(document.content)
        self.index.add([document.embedding])
        self.documents.append(document)
    
    def search(self, query: str, k: int = 3) -> List[IncidentDocument]:
        """Search for similar documents"""
        query_embedding = self.embedding_model.embed_query(query)
        D, I = self.index.search([query_embedding], k)
        return [self.documents[i] for i in I[0]]
