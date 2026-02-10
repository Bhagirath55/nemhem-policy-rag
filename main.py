from app.llm.groq_client import get_llm
from app.retrieval.vectorstore import get_vectorstore
from app.retrieval.retrieve import retrieve_json_and_pdf
from app.rag.rag_engine import rag_answer
from langchain_community.vectorstores import Chroma


def main():
    llm = get_llm()
    vectorstore = get_vectorstore()

    print("System ready.")
    print("Documents:", vectorstore._collection.count())
    docs = vectorstore.similarity_search("penalty", k=5)
    for d in docs:
        print(d.metadata)

    print("🔎 DIRECT CHROMA TEST")

    test_vs = Chroma(
        persist_directory=r"C:\Users\bhagi\Desktop\NemHemAI\policy-rag\notebooks\Data\vector_store",
        collection_name="policy_documents"
    )

    print("📦 DIRECT LOAD COUNT:", test_vs._collection.count())
    print("🔎 SAMPLE DOC:", test_vs._collection.peek())

    while True:
        query = input("\nEnter query (or 'exit'): ")
        if query.lower() == "exit":
            break

        docs = retrieve_json_and_pdf(vectorstore, query)
        result = rag_answer(query, docs, llm)

        print("\n--- RESPONSE ---")
        print(result["answer"])


if __name__ == "__main__":
    main()
