from rag_pipeline import RAGPipeline


rag = RAGPipeline(top_k=3)

question = "When was NovaTech founded and who founded it?"

result = rag.answer(question)

print("Question:", result["question"])

print("\nAnswer:")
print(result["answer"])

print("\nRetrieved chunks:")

for i, chunk in enumerate(result["retrieved_chunks"], start=1):
    print(f"\nResult {i}")
    print("Document:", chunk["document_id"])
    print("Distance:", chunk["distance"])
    print("Text:", chunk["text"])