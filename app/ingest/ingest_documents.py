import os
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    JSONLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import BASE_DIR
from app.retrieval.vectorstore import get_vectorstore


def main():
    print("📂 BASE_DIR:", BASE_DIR)

    # ----------------------------
    # 1. Get Vector Store (ABSTRACTED)
    # ----------------------------
    vectorstore = get_vectorstore()

    existing_count = vectorstore.count()

    if existing_count > 0:
        print(f"⚠️ Vector store already contains {existing_count} documents.")
        print("❌ Ingestion aborted to prevent duplicate insertion.")
        return

    print("✅ Vector store empty. Safe to ingest.")

    # ----------------------------
    # 2. Load PDFs (Contextual)
    # ----------------------------
    pdf_loader = DirectoryLoader(
        path=os.path.join(BASE_DIR, "data", "pdf_files"),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
    )

    pdf_docs = pdf_loader.load()

    for doc in pdf_docs:
        doc.metadata.update({
            "source_type": "pdf",
            "authority_level": "contextual",
            "document_class": "reference",
        })

    print(f"📄 PDF docs loaded: {len(pdf_docs)}")

    # ----------------------------
    # 3. Load JSON (Statutory)
    # ----------------------------
    json_loader = DirectoryLoader(
        path=os.path.join(BASE_DIR, "data", "json_files"),
        glob="**/*.json",
        loader_cls=JSONLoader,
        loader_kwargs={
            "jq_schema": ".. | strings",
            "text_content": True,
        },
    )

    json_docs = json_loader.load()

    for doc in json_docs:
        doc.metadata.update({
            "source_type": "json",
            "authority_level": "statutory",
            "document_class": "act",
        })

    print(f"🧾 JSON docs loaded: {len(json_docs)}")

    # ----------------------------
    # 4. Merge Documents
    # ----------------------------
    documents = pdf_docs + json_docs
    print(f"📚 Total raw documents: {len(documents)}")

    # ----------------------------
    # 5. Chunk (Metadata Preserved)
    # ----------------------------
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"✂️ Total chunks created: {len(chunks)}")

    # ----------------------------
    # 6. Store via Vector Store Interface
    # ----------------------------
    BATCH_SIZE = 500

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        print(f"➡️ Inserting batch {i // BATCH_SIZE + 1}")
        vectorstore.add_documents(batch)

    print("✅ INGESTION COMPLETE")
    print("📦 Final document count:", vectorstore.count())


if __name__ == "__main__":
    main()
