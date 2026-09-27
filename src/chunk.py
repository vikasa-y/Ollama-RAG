import pymupdf
import re

pdf_path = "Documents/Git_Handbook_Cleaned.pdf"

pdf = pymupdf.open(pdf_path)

text = ""

for page in pdf:

    page_text = page.get_text()

    if page_text:
        text += page_text + "\n"


print("Number of pages:", pdf.page_count)
print("Raw characters:", len(text))



# Remove excessive spaces and tabs
clean_text = re.sub(r"[ \t]+", " ", text)

# Remove spaces from empty lines
clean_text = re.sub(r"\n[ \t]+\n", "\n\n", clean_text)

# Reduce 3+ consecutive newlines to 2
clean_text = re.sub(r"\n{3,}", "\n\n", clean_text)

# Remove leading/trailing whitespace
clean_text = clean_text.strip()


print("Cleaned characters:", len(clean_text))



paragraphs = clean_text.split("\n\n")

paragraphs = [
    paragraph.strip()
    for paragraph in paragraphs
    if paragraph.strip()
]


print("Number of paragraphs:", len(paragraphs))


chunk_size = 1000
chunk_overlap = 200


text_units = []

for paragraph in paragraphs:

    # Normal paragraph
    if len(paragraph) <= chunk_size:

        text_units.append(paragraph)

    # Very large paragraph
    else:

        # Split large paragraph into sentences
        sentences = re.split(
            r"(?<=[.!?])\s+",
            paragraph
        )

        for sentence in sentences:

            sentence = sentence.strip()

            if sentence:
                text_units.append(sentence)


def get_overlap(text, overlap_size):

    # Take approximately the last 200 characters
    overlap = text[-overlap_size:]

    # Try to start at a word boundary
    space_position = overlap.find(" ")

    if space_position != -1:

        overlap = overlap[space_position + 1:]


    return overlap.strip()


chunks = []
current_chunk = ""


for unit in text_units:

    # --------------------------------------------------------
    # Unit fits into current chunk
    # --------------------------------------------------------

    if len(current_chunk) + len(unit) + 2 <= chunk_size:

        if current_chunk:

            current_chunk += "\n\n"

        current_chunk += unit


    # --------------------------------------------------------
    # Unit does NOT fit
    # --------------------------------------------------------

    else:

        # Save current chunk
        if current_chunk:

            chunks.append(current_chunk)


        # Create natural overlap
        overlap_text = get_overlap(
            current_chunk,
            chunk_overlap
        )


        # Start next chunk
        if overlap_text:

            current_chunk = (
                overlap_text
                + "\n\n"
                + unit
            )

        else:

            current_chunk = unit


if current_chunk:

    chunks.append(current_chunk)



print("\n==============================")
print("FINAL CHUNK INFORMATION")
print("==============================")

print("Chunk size:", chunk_size)
print("Chunk overlap:", chunk_overlap)
print("Number of chunks:", len(chunks))

chunk_lengths = [
    len(chunk)
    for chunk in chunks
]

print("\n==============================")
print("CHUNK SIZE STATISTICS")
print("==============================")

print("Smallest chunk:", min(chunk_lengths))
print("Largest chunk :", max(chunk_lengths))
print(
    "Average chunk :",
    round(sum(chunk_lengths) / len(chunk_lengths), 2)
)

for i, chunk in enumerate(chunks[:5]):

    print("\n")
    print("=" * 60)
    print(f"CHUNK {i}")
    print("=" * 60)

    print(chunk)

    print("\nCharacters:", len(chunk))


import json
from pathlib import Path


# ============================================
# SAVE CHUNKS TO JSON
# ============================================

output_path = Path("data/chunks.json")

# Create data folder if it doesn't exist
output_path.parent.mkdir(parents=True, exist_ok=True)


chunk_data = []

for i, chunk in enumerate(chunks):

    chunk_data.append({
        "chunk_id": i,
        "text": chunk,
        "length": len(chunk)
    })


with open(output_path, "w", encoding="utf-8") as file:

    json.dump(
        chunk_data,
        file,
        indent=4,
        ensure_ascii=False
    )


print("Chunks saved successfully!")
print("File:", output_path)
print("Number of chunks:", len(chunk_data))