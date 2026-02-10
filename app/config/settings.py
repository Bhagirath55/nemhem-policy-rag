import os
from dotenv import load_dotenv

load_dotenv()

# This MUST resolve to POLICY_RAG2
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

# 🔑 IMPORTANT: point to the EXISTING Chroma DB
VECTOR_DB_PATH = os.path.join(
    BASE_DIR,
    "notebooks",
    "Data",
    "vector_store"
)

COLLECTION_NAME = "policy_documents_final"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ---- DEBUG PRINTS (TEMPORARY) ----
print("🔍 BASE_DIR:", BASE_DIR)
print("🔍 VECTOR_DB_PATH:", VECTOR_DB_PATH)
