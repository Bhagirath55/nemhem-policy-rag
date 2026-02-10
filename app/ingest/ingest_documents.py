import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config.settings import VECTOR_DB_PATH, COLLECTION_NAME, BASE_DIR

print("📂 BASE_DIR:", BASE_DIR)
print("📦 VECTOR_DB_PATH:", VECTOR_DB_PATH)

# ----------------------------
# 0. Embeddings
# ----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs={"batch_size": 16},
)

# ----------------------------
# 1. SAFETY GUARD (CRITICAL)
# ----------------------------
vectorstore_check = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=VECTOR_DB_PATH,
)

existing_count = vectorstore_check._collection.count()

if existing_count > 0:
    print(f"⚠️ Collection '{COLLECTION_NAME}' already contains {existing_count} documents.")
    print("❌ Ingestion aborted to prevent duplicate insertion.")
    exit(0)

print("✅ Vector store empty. Safe to ingest.")

# ----------------------------
# 2. Load PDFs (Contextual / Non-binding)
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
        "authority_level": "contextual",      # LOW AUTHORITY
        "document_class": "reference",
    })

print(f"📄 PDF docs loaded: {len(pdf_docs)}")

# ----------------------------
# 3. Load JSON (Acts / Statutory)
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
        "authority_level": "statutory",       # HIGH AUTHORITY
        "document_class": "act",
    })

print(f"🧾 JSON docs loaded: {len(json_docs)}")

# ----------------------------
# 4. Merge documents
# ----------------------------
documents = pdf_docs + json_docs
print(f"📚 Total raw documents: {len(documents)}")

# ----------------------------
# 5. Chunk (metadata preserved)
# ----------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(documents)
print(f"✂️ Total chunks created: {len(chunks)}")

# ----------------------------
# 6. Embed + Store (BATCHED)
# ----------------------------
vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=VECTOR_DB_PATH,
)

BATCH_SIZE = 500

for i in range(0, len(chunks), BATCH_SIZE):
    batch = chunks[i:i + BATCH_SIZE]
    print(f"➡️ Inserting batch {i // BATCH_SIZE + 1}")
    vectorstore.add_documents(batch)

vectorstore.persist()

print("✅ INGESTION COMPLETE")
print("📦 Final document count:", vectorstore._collection.count())
