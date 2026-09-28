import json
from pathlib import Path
from ollama import embed


add_path = Path("Data/chunks.json")

with open(add_path , "r" , encoding="utf-8") as file:
    chunk_data = json.load(file)

print("Number of chunk:" , len(chunk_data))

texts =[item["text"] for item in chunk_data]



response = embed(
    model="nomic-embed-text" , input=texts
)

embeddings = response["embeddings"]

print("Number of embeddings:", len(embeddings))
print("Embedding dimensions:", len(embeddings[0]))


embedded_chunks = []

for chunk, embedding in zip(chunk_data, embeddings):
    embedded_chunks.append({
        "chunk_id": chunk["chunk_id"],
        "text": chunk["text"],
        "length": chunk["length"],
        "embedding": embedding
    })

output_path = Path("data/embeddings.json")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(
        embedded_chunks,
        file,
        indent=4,
        ensure_ascii=False
    )


print("\nEmbeddings saved successfully!")
print("File:", output_path)
print("Chunks:", len(embedded_chunks))
print("Dimensions:", len(embedded_chunks[0]["embedding"]))