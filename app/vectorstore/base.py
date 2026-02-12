from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document


class BaseVectorStore(ABC):

    @abstractmethod
    def add_documents(self, documents: List[Document]):
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 5):
        pass

    @abstractmethod
    def count(self) -> int:
        pass
