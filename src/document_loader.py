from pathlib import Path


def load_documents(directory="data/documents"):
    documents = []

    for file_path in sorted(Path(directory).glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "document_id": file_path.name,
            "text": text
        })

    return documents