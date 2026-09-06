from .document_loader import load_documents
from .chunker import chunk_documents
from .embeddings import Embedder
from .vector_store import VectorStore


def index_documents(
    chunk_size=80,
    overlap=20,
    collection_name="rag_documents"
):
    documents = load_documents()

    chunks = chunk_documents(
        documents,
        chunk_size=chunk_size,
        overlap=overlap
    )

    embedder = Embedder()

    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedder.embed_documents(texts)

    vector_store = VectorStore(
        collection_name=collection_name
    )

    vector_store.add_chunks(
        chunks,
        embeddings
    )

    print(f"Documents indexed: {len(documents)}")
    print(f"Chunks indexed: {len(chunks)}")
    print(f"Embeddings created: {len(embeddings)}")