# LEGACY MODULE – Will be deprecated after deterministic + hybrid migration

from langchain_chroma import Chroma
from app.vectorstore.base import BaseVectorStore
from app.config.settings import (VECTOR_DB_PATH, COLLECTION_NAME, EMBEDDINGS)


class ChromaVectorStore(BaseVectorStore):
    def __init__(self):
        self._store = Chroma(
            persist_directory=VECTOR_DB_PATH,
            collection_name=COLLECTION_NAME,
            embedding_function=EMBEDDINGS
        )

    def add_documents(self, documents):
        self._store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 5):
        return self._store.similarity_search(query, k=k)

    def count(self) -> int:
        return self._store._collection.count()
