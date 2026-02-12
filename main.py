from app.llm.groq_client import get_llm
from app.retrieval.vectorstore import get_vectorstore
from app.retrieval.retrieve import retrieve_json_and_pdf
from app.rag.rag_engine import rag_answer


def main():
    llm = get_llm()
    vectorstore = get_vectorstore()

    print("System ready.")
    print("Documents:", vectorstore.count())

    # 🔎 TEMP METADATA TEST
    print("\n🔎 METADATA TEST")

    docs = vectorstore.similarity_search("leave", k=2)

    for d in docs:
        print("\nCONTENT PREVIEW:")
        print(d.page_content[:200])

        print("\nMETADATA:")
        print(d.metadata)

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
