from retriever import Retriever
from evaluators.retrieval import evaluate_retrieval


retriever = Retriever(top_k=3)

query = "Which platform serves machine learning predictions at high throughput?"

results = retriever.retrieve(query)

evaluation = evaluate_retrieval(
    results,
    relevant_source="company_09.txt"
)

print("Query:", query)

print("\nRetrieved documents:")

for result in results:
    print("-", result["document_id"])

print("\nRetrieval evaluation:")
print("Precision:", evaluation["precision"])
print("Recall:", evaluation["recall"])