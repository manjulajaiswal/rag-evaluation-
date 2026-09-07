from .embeddings import Embedder
from .vector_store import VectorStore


class Retriever:
    def __init__(
        self,
        top_k=3,
        collection_name="rag_documents",
        embedding_model="sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.embedder = Embedder(
            model_name=embedding_model
        )

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


if __name__ == "__main__":
    retriever = Retriever(
    top_k=3,
    collection_name="rag_chunk_small",
    embedding_model="sentence-transformers/all-MiniLM-L6-v2"
)

    query = "What is TrackNet used for in badminton video analysis?"

    results = retriever.retrieve(query)

    print("\nQuery:")
    print(query)

    print("\nRetrieved chunks:")

    for i, result in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print("Document:", result["document_id"])
        print("Distance:", result["distance"])
        print("Text:", result["text"])