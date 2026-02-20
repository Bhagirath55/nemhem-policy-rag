import os
import json

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_core.documents import Document

from app.config.settings import BASE_DIR
from app.retrieval.vectorstore import get_vectorstore
from app.utils.id_generator import generate_section_id


# =========================================================
# 🔹 Recursive paragraph extractor
# =========================================================

def extract_paragraph_text(para):

    if isinstance(para, str):
        return para

    if isinstance(para, dict):

        text = ""

        if "text" in para:
            text += para["text"] + "\n"

        if "contains" in para:
            for sub in para["contains"].values():
                text += extract_paragraph_text(sub) + "\n"

        return text.strip()

    return ""


# =========================================================
# 🔹 Parse Legal JSON
# =========================================================

def parse_legal_json(file_path):

    documents = []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    act_title = data.get("Act Title", "Unknown Act")
    act_id = data.get("Act ID", "Unknown_ID")

    # =====================================================
    # CASE 1 → JSON HAS PARTS
    # =====================================================
    
    if "Parts" in data:

        parts = data.get("Parts", {})

        for part in parts.values():

            part_name = part.get("Name", "Unknown Part")
            sections = part.get("Sections", {})

            for section_number, section in sections.items():

                section_heading = section.get("heading", "")
                paragraphs = section.get("paragraphs", {})

                full_text = f"{section_number} {section_heading}\n\n"

                for para in paragraphs.values():
                    full_text += extract_paragraph_text(para) + "\n"

                if full_text.strip():

                    # 🔥 Generate section_id
                    section_id = generate_section_id(
                        act_id=act_id, section_number=section_number
                    )

                    documents.append(
                        Document(
                            page_content=full_text.strip(),
                            metadata={
                                "act_title": act_title,
                                "act_id": act_id,
                                "section_id": section_id,  # ✅ IMPORTANT
                                "part": part_name,
                                "section_number": section_number,
                                "section_heading": section_heading,
                                "authority_level": "statutory",
                                "source_type": "json",
                                "source": file_path,
                            },
                        )
                    )

    # =====================================================
    # CASE 2 → JSON HAS CHAPTERS
    # =====================================================
    elif "Chapters" in data:

        chapters = data.get("Chapters", {})

        for chapter in chapters.values():

            chapter_name = chapter.get("Name", "Unknown Chapter")
            sections = chapter.get("Sections", {})

            for section_number, section in sections.items():

                section_heading = section.get("heading", "")
                paragraphs = section.get("paragraphs", {})

                full_text = f"{section_number} {section_heading}\n\n"

                for para in paragraphs.values():
                    full_text += extract_paragraph_text(para) + "\n"

                if full_text.strip():

                    # 🔥 Generate section_id
                    section_id = generate_section_id(
                        act_id=act_id, section_number=section_number
                    )

                    documents.append(
                        Document(
                            page_content=full_text.strip(),
                            metadata={
                                "act_title": act_title,
                                "act_id": act_id,
                                "section_id": section_id,  # ✅ IMPORTANT
                                "chapter": chapter_name,
                                "section_number": section_number,
                                "section_heading": section_heading,
                                "authority_level": "statutory",
                                "source_type": "json",
                                "source": file_path,
                            },
                        )
                    )

    return documents


# =========================================================
# 🔹 MAIN INGESTION PIPELINE
# =========================================================


def main():

    print("📂 BASE_DIR:", BASE_DIR)

    vectorstore = get_vectorstore()

    if vectorstore.count() > 0:
        print("❌ Vector store not empty. Aborting to prevent duplicates.")
        return

    print("✅ Vector store empty. Safe to ingest.")

    # =====================================================
    # 1. LOAD PDFs
    # =====================================================
    pdf_loader = DirectoryLoader(
        path=os.path.join(BASE_DIR, "data", "pdf_files"),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
    )

    pdf_docs = pdf_loader.load()

    for doc in pdf_docs:
        doc.metadata.update(
            {
                "source_type": "pdf",
                "authority_level": "contextual",
                "document_class": "reference",
            }
        )

    print(f"📄 PDF docs loaded: {len(pdf_docs)}")

    # =====================================================
    # 2. LOAD JSON FILES
    # =====================================================
    json_dir = os.path.join(BASE_DIR, "data", "json_files")
    json_docs = []

    for file in os.listdir(json_dir):
        if file.endswith(".json"):
            file_path = os.path.join(json_dir, file)
            print(f"📄 Parsing JSON file: {file}")
            json_docs.extend(parse_legal_json(file_path))

    print(f"🧾 JSON sections extracted: {len(json_docs)}")

    documents = pdf_docs + json_docs
    print(f"📚 Total raw documents: {len(documents)}")

    # =====================================================
    # 3. CHUNKING
    # =====================================================
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
    )

    chunks = text_splitter.split_documents(documents)

    print(f"✂️ Total chunks created: {len(chunks)}")

    # 🔥 ENSURE section_id EXISTS IN EVERY JSON CHUNK
    for chunk in chunks:
        if chunk.metadata.get("source_type") == "json":
            if "section_id" not in chunk.metadata:
                raise ValueError("❌ section_id missing in JSON chunk metadata")

    # =====================================================
    # 4. INSERT INTO VECTOR STORE
    # =====================================================
    
    BATCH_SIZE = 500

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        print(f"➡️ Inserting batch {i // BATCH_SIZE + 1}")
        vectorstore.add_documents(batch)

    print("✅ INGESTION COMPLETE")
    print("📦 Final document count:", vectorstore.count())


if __name__ == "__main__":
    main()
