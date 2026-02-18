# LEGACY MODULE – Will be deprecated after deterministic + hybrid migration

from langchain_groq import ChatGroq
from app.config.settings import GROQ_API_KEY


def get_llm():
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama-3.1-8b-instant",
        temperature=0.1,
        max_tokens=1024,
    )
