def evaluate_retrieval(retrieved_chunks, relevant_sources):
    retrieved_documents = [
        chunk["document_id"]
        for chunk in retrieved_chunks
    ]

    relevant_retrieved = sum(
        1
        for document_id in retrieved_documents
        if document_id in relevant_sources
    )

    total_retrieved = len(retrieved_documents)
    total_relevant = len(relevant_sources)

    precision = (
        relevant_retrieved / total_retrieved
        if total_retrieved > 0
        else 0
    )

    retrieved_relevant_sources = set(
        document_id
        for document_id in retrieved_documents
        if document_id in relevant_sources
    )

    recall = (
        len(retrieved_relevant_sources) / total_relevant
        if total_relevant > 0
        else 0
    )

    return {
        "precision": precision,
        "recall": recall
    }