import json
from pathlib import Path
from ollama import embed


# Load stored chunk embeddings
input_path = Path("data/embeddings.json")

with open(input_path, "r", encoding="utf-8") as file:
    embedded_chunks = json.load(file)

print("Loaded chunks:", len(embedded_chunks))


# Ask the user a question
question = input("\nAsk a question: ")


# Convert the question into an embedding
response = embed(
    model="nomic-embed-text",
    input=question
)

question_embedding = response["embeddings"][0]

print("Question embedding dimensions:", len(question_embedding))

import math


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    return dot_product / (magnitude_a * magnitude_b)


def retrieve(question_embedding, embedded_chunks, top_k=5):
    results = []

    for chunk in embedded_chunks:
        score = cosine_similarity(
            question_embedding,
            chunk["embedding"]
        )

        results.append({
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "score": score
        })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )
    return results[:top_k]

results = retrieve(
    question_embedding,
    embedded_chunks,
    top_k=5
)

for result in results:
    print("=" * 60)
    print("Chunk ID:", result["chunk_id"])
    print("Similarity:", round(result["score"], 4))
    print(result["text"])