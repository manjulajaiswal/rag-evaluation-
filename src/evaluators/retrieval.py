def evaluate_retrieval(retrieved_chunks, relevant_source):
    retrieved_documents = [
        chunk["document_id"]
        for chunk in retrieved_chunks
    ]

    relevant_retrieved = sum(
        1
        for document_id in retrieved_documents
        if document_id == relevant_source
    )

    total_retrieved = len(retrieved_documents)

    precision = (
        relevant_retrieved / total_retrieved
        if total_retrieved > 0
        else 0
    )

    recall = 1 if relevant_source in retrieved_documents else 0

    return {
        "precision": precision,
        "recall": recall
    }