from document_loader import load_documents
from chunker import chunk_documents


documents = load_documents()

all_chunks = chunk_documents(
    documents,
    chunk_size=80,
    overlap=20
)

print("Documents:", len(documents))
print("Total chunks:", len(all_chunks))

print("\nFirst 3 chunks:\n")

for chunk in all_chunks[:3]:
    print("Chunk ID:", chunk["chunk_id"])
    print("Document:", chunk["document_id"])
    print("Text:", chunk["text"])
    print("-" * 60)