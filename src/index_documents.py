import json

from .document_loader import load_documents
from .chunker import chunk_documents
from .embeddings import Embedder
from .vector_store import VectorStore


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


def index_documents(config_path, collection_name):
    config = load_config(config_path)

    documents = load_documents()

    chunks = chunk_documents(
        documents,
        chunk_size=config["chunk_size"],
        overlap=config["overlap"]
    )

    embedder = Embedder(
        model_name=config["embedding_model"]
    )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embedder.embed_documents(texts)

    vector_store = VectorStore(
        collection_name=collection_name
    )

    vector_store.add_chunks(
        chunks,
        embeddings
    )

    print(f"Configuration: {config['config_name']}")
    print(f"Documents indexed: {len(documents)}")
    print(f"Chunks indexed: {len(chunks)}")
    print(f"Embedding model: {config['embedding_model']}")
    print(f"Embedding dimension: {embeddings.shape[1]}")

if __name__ == "__main__":
    import sys

    config_path = sys.argv[1]

    config = load_config(config_path)

    collection_name = f"rag_{config['config_name']}"

    index_documents(
        config_path,
        collection_name
    )