from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config.settings import VECTOR_DB_PATH, COLLECTION_NAME

_embeddings = None

def get_embeddings():
    print("🔍 VECTOR_DB_PATH being used:")
    print(VECTOR_DB_PATH)
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            encode_kwargs={"batch_size": 16},
        )
    return _embeddings


def get_vectorstore():
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=VECTOR_DB_PATH,
    )
    return vectorstore
