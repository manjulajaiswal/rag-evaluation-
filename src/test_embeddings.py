from embeddings import Embedder


embedder = Embedder()

documents = [
    "NovaTech was founded in 2018.",
    "NovaTech launched Orion for real-time machine learning inference."
]

document_embeddings = embedder.embed_documents(documents)

query_embedding = embedder.embed_query(
    "When was NovaTech founded?"
)

print("Document embeddings shape:", document_embeddings.shape)
print("Query embedding shape:", query_embedding.shape)