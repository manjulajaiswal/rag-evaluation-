import chromadb


class VectorStore:
    def __init__(
        self,
        collection_name="rag_documents"
    ):
        self.client = chromadb.PersistentClient(
            path="results/chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_chunks(self, chunks, embeddings):
        self.collection.upsert(
            ids=[chunk["chunk_id"] for chunk in chunks],
            documents=[chunk["text"] for chunk in chunks],
            embeddings=embeddings.tolist(),
            metadatas=[
                {"document_id": chunk["document_id"]}
                for chunk in chunks
            ]
        )

    def search(self, query_embedding, top_k=3):
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )

        return results