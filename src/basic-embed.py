from ollama import embed

texts = [
    "Git is a distributed version control system.",
    "Git helps developers track changes in their code.",
    "The weather is very hot today."
]

response = embed(
    model="nomic-embed-text",
      input=texts
      )

embeddings = response["embeddings"][0]


embeddings = response["embeddings"]

for i, vector in enumerate(embeddings):
    print(f"Text {i}")
    print("Dimensions:", len(vector))
    print("First 5 values:", vector[:5])
    print()