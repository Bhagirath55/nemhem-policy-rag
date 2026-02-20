import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("sections")

def add_section_embedding(section_id, text):
    collection.add(
        documents=[text],
        metadatas=[{"section_id": section_id}],
        ids=[section_id]
    )

def query_embedding(query_text):
    return collection.query(
        query_texts=[query_text],
        n_results=1
    )
