from app.llm.groq_client import get_llm
from app.retrieval.vectorstore import get_vectorstore
from app.retrieval.retrieve import retrieve_json_and_pdf
from app.rag.rag_engine import rag_answer


def main():
    llm = get_llm()
    vectorstore = get_vectorstore()

    print("System ready.")
    print("Documents:", vectorstore.count())

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
