from app.rag.context_builder import build_context_and_sources

def rag_answer(query, docs, llm):
    if not docs:
        return {
            "answer": (
                "Based on the available records, no relevant provisions "
                "were identified. Further clarification may be required."
            ),
            "sources": [],
        }

    context, sources = build_context_and_sources(docs)

    prompt = f"""
You are an administrative decision-support system.
You do not approve, reject, or recommend actions.

Explain:
- what can be concluded,
- what cannot be concluded,
- what requires further confirmation.

Sources:
{context}

Query:
{query}

Structured Response:
""".strip()

    response = llm.invoke(prompt)

    return {
        "answer": response.content.strip(),
        "sources": sources
    }
