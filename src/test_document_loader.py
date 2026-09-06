from document_loader import load_documents

documents = load_documents()

print("Number of documents:", len(documents))

for document in documents:
    print(
        document["document_id"],
        "->",
        len(document["text"].split()),
        "words"
    )