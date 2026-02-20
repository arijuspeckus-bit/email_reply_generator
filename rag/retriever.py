import numpy as np
from .embeddings import embed_texts

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def build_index(documents):

    chunks = []
    metadata = []

    for doc in documents:
        split = chunk_text(doc["text"])
        for i, chunk in enumerate(split):
            chunks.append(chunk)
            metadata.append({
                "filename": doc["filename"],
                "chunk_id": i
            })

    embeddings = embed_texts(chunks)

    return chunks, embeddings, metadata

def retrieve(query, chunks, embeddings, metadata, k=3):

    query_embedding = embed_texts([query])[0]

    similarities = np.dot(embeddings, query_embedding)

    top_indices = np.argsort(similarities)[-k:][::-1]

    results = []
    for idx in top_indices:
        results.append({
            "text": chunks[idx],
            "filename": metadata[idx]["filename"],
            "chunk_id": metadata[idx]["chunk_id"]
        })

    return results