from langchain_community.vectorstores import Chroma
from app.config.settings import (VECTOR_DB_PATH, COLLECTION_NAME, EMBEDDINGS)


def retrieve_json_and_pdf(
        vectorstore,
        query: str,
        k_json: int = 4,
        k_pdf: int = 2,
        fetch_k: int = 30,
):
    docs = vectorstore.similarity_search(query, k=fetch_k)

    json_docs = []
    pdf_docs = []

    for d in docs:
        source = d.metadata.get("source", "").lower()

        if "json" in source and len(json_docs) < k_json:
            json_docs.append(d)
        elif "pdf" in source and len(pdf_docs) < k_pdf:
            pdf_docs.append(d)

        if len(json_docs) == k_json and len(pdf_docs) == k_pdf:
            break

    return json_docs + pdf_docs
