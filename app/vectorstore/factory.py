# LEGACY MODULE – Will be deprecated after deterministic + hybrid migration

from app.vectorstore.chroma_store import ChromaVectorStore


def get_vectorstore():
    return ChromaVectorStore()
