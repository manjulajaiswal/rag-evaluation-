from .embeddings import Embedder
from .vector_store import VectorStore


class Retriever:
    def __init__(self, top_k=3, collection_name="rag_documents"):
        self.embedder = Embedder()
        self.vector_store = VectorStore(
        collection_name=collection_name
    )
        self.top_k = top_k

    def retrieve(self, query):
        query_embedding = self.embedder.embed_query(query)

        results = self.vector_store.search(
            query_embedding,
            top_k=self.top_k
        )

        retrieved_chunks = []

        for i in range(len(results["documents"][0])):
            retrieved_chunks.append({
                "chunk_id": results["ids"][0][i],
                "document_id": results["metadatas"][0][i]["document_id"],
                "text": results["documents"][0][i],
                "distance": results["distances"][0][i]
            })

        return retrieved_chunks