def build_context_and_sources(docs):
    context_blocks = []
    sources = []

    for i, doc in enumerate(docs, 1):
        meta = doc.metadata

        context_blocks.append(f"""
[Source {i}]
Type: {meta.get("source_type")}
File: {meta.get("source")}
Page: {meta.get("page", meta.get("page_label", "N/A"))}

{doc.page_content.strip()}
""".strip())

        sources.append({
            "type": meta.get("source_type"),
            "file": meta.get("source"),
            "page": meta.get("page", meta.get("page_label")),
            "preview": doc.page_content[:120] + "..."
        })

    return "\n\n".join(context_blocks), sources
