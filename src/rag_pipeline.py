from .retriever import Retriever
from .generator import Generator


class RAGPipeline:
    def __init__(
        self,
        top_k=3,
        collection_name="rag_documents",
        embedding_model="sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.retriever = Retriever(
            top_k=top_k,
            collection_name=collection_name,
            embedding_model=embedding_model
        )

        self.generator = Generator()

    def answer(self, question):
        retrieved_chunks = self.retriever.retrieve(question)

        context = "\n\n".join(
            chunk["text"] for chunk in retrieved_chunks
        )

        answer = self.generator.generate(
            question,
            context
        )

        return {
            "question": question,
            "answer": answer,
            "retrieved_chunks": retrieved_chunks
        }