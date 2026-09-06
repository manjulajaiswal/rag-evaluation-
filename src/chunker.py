def chunk_text(text, chunk_size=80, overlap=20):
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def chunk_documents(documents, chunk_size=80, overlap=20):
    all_chunks = []

    for document in documents:
        chunks = chunk_text(
            document["text"],
            chunk_size=chunk_size,
            overlap=overlap
        )

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_id": f'{document["document_id"]}_{i}',
                "document_id": document["document_id"],
                "text": chunk
            })

    return all_chunks