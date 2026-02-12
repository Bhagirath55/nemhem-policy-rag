import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# =========================
# Base Paths
# =========================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

# =========================
# Vector Store Configuration
# =========================

VECTOR_DB_PATH = os.path.join(
    BASE_DIR,
    "notebooks",
    "Data",
    "vector_store"
)

COLLECTION_NAME = "policy_documents_final"

# =========================
# Embedding Configuration
# =========================

EMBEDDINGS = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =========================
# LLM / API Keys
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ---- DEBUG PRINTS (TEMPORARY) ----
print("🔍 BASE_DIR:", BASE_DIR)
print("🔍 VECTOR_DB_PATH:", VECTOR_DB_PATH)
