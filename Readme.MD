# Basic RAG System Using Ollama

A beginner-friendly Retrieval-Augmented Generation (RAG) project built using Python, Ollama, and Llama 3.2. This project explores how to retrieve relevant information from a PDF and use it to generate answers with a local LLM.

## About the Project

This is an experimental RAG implementation created for learning purposes. It uses a single Git handbook PDF to demonstrate the basic RAG workflow, from extracting text to generating answers.

The project is a working example of the core RAG pipeline, not a production-ready application.

## What Is RAG?

Retrieval-Augmented Generation (RAG) combines information retrieval with a Large Language Model (LLM).

Instead of relying only on the model's existing knowledge, RAG retrieves relevant information from an external source and provides it as context for generating an answer.

## Workflow

```text
PDF Document
     ↓
Text Extraction
     ↓
Text Cleaning
     ↓
Text Chunking
     ↓
Generate Embeddings
     ↓
Store Chunks and Embeddings
     ↓
Embed User Question
     ↓
Similarity Search
     ↓
Retrieve Top 5 Chunks
     ↓
Build Prompt with Context
     ↓
Llama 3.2
     ↓
Generated Answer
```

## Technologies Used

- **Python** — pipeline implementation
- **PyMuPDF** — PDF text extraction
- **Ollama** — running models locally
- **nomic-embed-text** — generating text embeddings
- **Llama 3.2** — generating answers
- **JSON** — storing chunks and embeddings
- **Cosine similarity** — ranking retrieved chunks

## Project Features

- Extracts text from a single PDF.
- Cleans extracted text and divides it into chunks.
- Generates embeddings for the chunks.
- Stores chunk text and embeddings in JSON.
- Converts user questions into embeddings.
- Retrieves the five highest-ranked chunks using cosine similarity.
- Builds a prompt from the retrieved context.
- Generates answers using Llama 3.2.

## Known Limitations

### 1. Imperfect Chunking

The current chunking implementation uses paragraph-based grouping, a target chunk size of approximately 1,000 characters, and an overlap of approximately 200 characters.

Although this creates usable chunks, it does not always preserve the document's full semantic structure. Related information may be separated across chunks, and some chunks may contain unrelated topics.

### 2. PDF Extraction Limitations

Some content in the PDF may be represented by diagrams, images, or layouts that are not fully captured by ordinary text extraction. For example, a question about the four areas in Git did not receive the expected answer, even though the relevant topic appeared in the extracted text.

The exact cause of the missing information has not been fully verified.

### 3. Retrieval Limitations

The system retrieves the top five chunks based on embedding similarity. The most relevant chunk may not rank highly enough to appear in those results.

As a result, the LLM may not receive the information needed to answer a question.

### 4. Answer Limitations

The LLM generates answers using the retrieved context. If relevant information is missing from that context, the model may fail to answer correctly or report that the answer could not be found.

## Future Improvements

These are potential improvements for future versions, not features currently implemented:

- Improve chunk boundaries and preserve document structure.
- Handle diagrams and other content that PDF text extraction may miss.
- Experiment with different chunk sizes and overlap strategies.
- Improve retrieval accuracy and evaluate different retrieval methods.
- Add source references to generated answers.
- Test the system with additional documents.
- Consider a dedicated vector database when the project requires it.

## What I Learned

Through this project, I explored:

- PDF text extraction and cleaning.
- Chunking and chunk overlap.
- Text embeddings and vector representations.
- Cosine similarity and top-K retrieval.
- Prompt construction using retrieved context.
- Connecting retrieval with a local LLM.
- Debugging retrieval failures by inspecting intermediate results.

## Project Status

**Status: Experimental learning prototype — basic RAG pipeline implemented.**

The system demonstrates the main stages of RAG but has known limitations in chunking, PDF extraction, and retrieval accuracy. These limitations are intentionally documented as areas for future learning and improvement.

## Bad Chunking: A Known Problem

One of the main limitations of this project is imperfect chunking.

The initial implementation divided the extracted PDF text into chunks using paragraph grouping, a target size of approximately 1,000 characters, and an overlap of approximately 200 characters.

Although this approach generated chunks successfully, it did not always preserve the document's semantic structure.

### Problems Observed

- **Topic mixing:** A single chunk could contain content from different sections or chapters.
- **Incomplete context:** Important information could be split across multiple chunks.
- **Poor chunk boundaries:** Chunk boundaries did not always align with meaningful sections or concepts.
- **Extraction artifacts:** PDF formatting, headings, and diagram-related text sometimes appeared in awkward positions.
- **Retrieval failures:** The correct information could exist in the stored chunks but fail to appear among the top five retrieved results.

### Real Example

When asked:

> Which are the four areas in Git?

The system returned unrelated chunks about Git repositories, configuration, and GitHub instead of the expected information.

A keyword search revealed that **Chunk 6** contained the sentence:

> Git moves your changes through four areas before they reach GitHub.

However, the expected answer was not successfully generated. The extracted text shown in the chunk did not include the names of all four areas, so the exact cause could not be confirmed.

This demonstrated that successful text extraction and embedding generation do not guarantee accurate retrieval or answers.

### What Could Be Improved?

- Preserve headings and section boundaries when splitting documents.
- Avoid combining unrelated topics in a single chunk.
- Handle long paragraphs and diagrams more carefully.
- Experiment with different chunk sizes and overlap lengths.
- Evaluate retrieval results against questions with known answers.

**Current decision:** Keep the existing implementation as a learning prototype. Improve chunking and retrieval in a future version after learning the necessary techniques.

This limitation is documented intentionally as part of the project's learning process.

## Conclusion

This project was built to understand the fundamental workflow of Retrieval-Augmented Generation through hands-on implementation. It serves as a starting point for learning how documents, embeddings, retrieval, and LLMs work together in a RAG system.