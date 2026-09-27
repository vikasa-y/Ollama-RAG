# Retrieval-Augmented Generation (RAG)

A practical implementation of **Retrieval-Augmented Generation (RAG)** using local documents, text processing, embeddings, vector search, and a Large Language Model (LLM).

The goal of this project is to understand how an AI system can answer questions using **external/private knowledge** instead of relying only on the information stored inside the LLM.

---

## What is RAG?

**RAG = Retrieval-Augmented Generation**

RAG is an architecture that combines:

* **Information Retrieval** — finds relevant information from an external knowledge base.
* **Augmentation** — adds the retrieved information to the user's prompt.
* **Generation** — an LLM generates the final response using the retrieved context.

Instead of asking an LLM to answer only from its pretrained knowledge, RAG first retrieves relevant information from a knowledge source and gives that information to the LLM as context.

The original RAG research introduced the idea of combining a pretrained language model with an external non-parametric memory represented by a dense vector index.

---

# Why Do We Need RAG?

A normal LLM has some limitations:

* It may not know private documents.
* Its knowledge may not contain recently created information.
* It can generate incorrect information when it does not have enough context.
* It cannot automatically know the contents of your personal files.
* Updating knowledge directly inside a model can require additional training.

RAG provides another approach:

```text
Your Documents
      ↓
Process & Index
      ↓
Knowledge Base
      ↓
User Question
      ↓
Retrieve Relevant Information
      ↓
Add Context to Prompt
      ↓
LLM
      ↓
Answer
```

RAG allows external knowledge to be updated without retraining the underlying LLM for every document change.

---

# RAG Workflow

The complete RAG workflow can be divided into two major phases:

## 1. Indexing Phase

This phase prepares the knowledge base.

```text
Documents
   ↓
Document Extraction
   ↓
Text Cleaning
   ↓
Chunking
   ↓
Embedding Generation
   ↓
Vector Database
```

### Step 1 — Documents

The knowledge source can contain:

* `.txt`
* PDF
* Markdown
* Documentation
* Books
* Notes
* Code
* Database records
* APIs
* Other structured or unstructured data

---

## Step 2 — Extraction

The system extracts usable text from the original documents.

Example:

```text
PDF
 ↓
Text Extraction
 ↓
Raw Text
```

For this project, document processing is separated from later stages so that the data pipeline remains easier to understand and maintain.

---

## Step 3 — Chunking

Large documents are divided into smaller pieces called **chunks**.

Example:

```text
Large Document
       ↓
 ┌─────────────┐
 │ Chunk 1     │
 ├─────────────┤
 │ Chunk 2     │
 ├─────────────┤
 │ Chunk 3     │
 ├─────────────┤
 │ Chunk 4     │
 └─────────────┘
```

### Why chunk?

A complete document may be too large or contain too much unrelated information for a single retrieval operation.

Smaller chunks allow the retrieval system to find the specific section that is relevant to a question.

Chunking strategy can affect retrieval quality because the retrieved text needs to contain enough useful context while still fitting efficiently into the model's context window.

---

# Step 4 — Embeddings

An **embedding** converts text into a numerical vector representing its semantic meaning.

For example:

```text
"Python is a programming language"
                 ↓
        Embedding Model
                 ↓
       [0.21, -0.13, 0.87, ...]
```

The vector is not simply a numerical version of the words. It represents relationships and semantic characteristics of the text.

Documents and user queries are converted into compatible vector representations so that they can be compared during retrieval.

---

# Step 5 — Vector Database

The generated embeddings are stored in a **vector database** or vector index.

Conceptually:

```text
Chunk
  +
Embedding
  +
Metadata
  ↓
Vector Store
```

The vector store allows the system to perform similarity searches over the stored embeddings.

Common similarity approaches include:

* Cosine similarity
* Dot product
* Euclidean distance

The exact method depends on the retrieval system and vector store being used.

---

# 2. Query Phase

Once the knowledge base has been created, users can ask questions.

```text
User Question
      ↓
Query Embedding
      ↓
Similarity Search
      ↓
Relevant Chunks
      ↓
Context
      ↓
Prompt + Context
      ↓
LLM
      ↓
Generated Answer
```

---

# Step 6 — User Query

Example:

```text
User:
"What are the main features described in the document?"
```

The question is converted into an embedding using the same compatible embedding process used for the document chunks.

---

# Step 7 — Retrieval

The query vector is compared with the stored document vectors.

The system searches for the chunks that are most semantically similar to the query.

Example:

```text
User Query
    ↓
Query Vector
    ↓
Similarity Search
    ↓
Top Relevant Chunks
```

This is the **Retrieval** part of Retrieval-Augmented Generation.

---

# Step 8 — Context Augmentation

The retrieved chunks are added to the user's question.

Conceptually:

```text
System Instructions
        +
Retrieved Context
        +
User Question
        ↓
     Prompt
```

Example:

```text
Context:
[Relevant document information]

Question:
What are the main features?

Instruction:
Answer using the provided context.
```

The retrieved information becomes additional context for the LLM.

---

# Step 9 — Generation

The augmented prompt is sent to the LLM.

```text
Prompt
  +
Retrieved Context
  ↓
 LLM
  ↓
Answer
```

The LLM uses the retrieved context to generate a natural-language response.

This is the **Generation** part of RAG.

---

# Complete RAG Architecture

```text
                    INDEXING PHASE
                    ==============

 Documents
     │
     ▼
 Document Extraction
     │
     ▼
 Text Cleaning
     │
     ▼
 Chunking
     │
     ▼
 Embedding Model
     │
     ▼
 Vector Embeddings
     │
     ▼
 Vector Database
     │
     │
     │
     │
     ▼
                 QUERY PHASE
                 ============

 User Question
     │
     ▼
 Query Embedding
     │
     ▼
 Similarity Search
     │
     ▼
 Relevant Chunks
     │
     ▼
 Context + User Question
     │
     ▼
      LLM
     │
     ▼
 Generated Answer
```

A standard RAG architecture follows this pattern: retrieve relevant information, add it to the prompt as context, and then generate the response using the LLM.

---

# Main Components of RAG

| Component       | Purpose                                            |
| --------------- | -------------------------------------------------- |
| Document Loader | Reads the original knowledge sources               |
| Text Extractor  | Converts documents into usable text                |
| Text Cleaner    | Removes unnecessary or problematic content         |
| Chunker         | Splits large text into smaller pieces              |
| Embedding Model | Converts text into vectors                         |
| Vector Store    | Stores and searches embeddings                     |
| Retriever       | Finds relevant chunks                              |
| Prompt          | Combines instructions, context and question        |
| LLM             | Generates the final response                       |
| Application     | Provides the interface between user and RAG system |

Production RAG systems can contain additional components such as connectors, metadata filtering, reranking, guardrails, orchestration, identity/access control, and user interfaces.

---

# What Does Each Part Actually Do?

## LLM

The LLM is responsible for **understanding the prompt and generating the answer**.

It is not necessarily responsible for searching your entire document collection.

---

## Embedding Model

The embedding model converts text into numerical vectors.

Its job is:

```text
Text → Vector
```

Both documents and queries need compatible embeddings for semantic retrieval.

---

## Vector Store

The vector store manages the embeddings and enables similarity search.

Its job is:

```text
Vectors → Search → Relevant Vectors
```

Vector databases are optimized for storing and querying high-dimensional vectors.

---

## Retriever

The retriever connects the user query with the knowledge base.

```text
Question
   ↓
Search
   ↓
Relevant Chunks
```

The retriever determines which pieces of information should be provided to the LLM.

---

## Generator

The generator is normally an LLM.

```text
Retrieved Context
       +
User Question
       ↓
      LLM
       ↓
    Answer
```

---

# RAG vs Normal LLM

### Normal LLM

```text
User Question
      ↓
     LLM
      ↓
   Answer
```

The model primarily relies on its learned parameters and whatever context is directly supplied in the conversation.

### RAG

```text
User Question
      ↓
 Retriever
      ↓
Relevant Knowledge
      ↓
Question + Context
      ↓
     LLM
      ↓
   Answer
```

RAG introduces an external retrieval layer before generation.

---

# RAG vs Fine-Tuning

RAG and fine-tuning solve different problems.

| RAG                                                       | Fine-Tuning                                                   |
| --------------------------------------------------------- | ------------------------------------------------------------- |
| Retrieves external information                            | Changes model behavior/parameters through additional training |
| Good for changing knowledge sources                       | Useful for adapting behavior, style, or task patterns         |
| Knowledge can be updated by updating the retrieval source | Updating knowledge may require another training process       |
| Uses external context during inference                    | Uses learned parameters after training                        |
| Requires retrieval infrastructure                         | Requires a training/fine-tuning workflow                      |

RAG is particularly useful when an application needs to work with external or changing knowledge without embedding all of that knowledge directly into the model.

---

# Where is RAG Used?

RAG can be useful for applications such as:

### 1. Document Question Answering

```text
Documents
    ↓
RAG
    ↓
Ask Questions
```

Users can ask questions about a collection of documents.

---

### 2. Private Knowledge Assistants

A company or individual can build an assistant around its own authorized knowledge sources.

Examples:

* Internal documentation
* Technical manuals
* Project documentation
* Policies
* Notes

---

### 3. Customer Support

A support system can retrieve relevant product documentation before generating an answer.

```text
Customer Question
       ↓
Product Documentation
       ↓
Relevant Context
       ↓
LLM
       ↓
Support Response
```

---

### 4. Research Assistants

RAG can retrieve relevant passages from a collection of research documents before generating an answer.

---

### 5. Code Documentation Assistants

A RAG system can retrieve relevant documentation or code sections before answering developer questions.

---

### 6. Educational Assistants

A knowledge base containing authorized course material can be used to answer questions using that material as context.

---

# Advantages of RAG

### External Knowledge

RAG can connect an LLM to information outside its original training data.

### Knowledge Updates

The knowledge base can be updated without necessarily retraining the underlying LLM.

### Domain-Specific Answers

The system can focus retrieval on a particular collection of documents.

### Reduced Irrelevant Context

Instead of sending an entire document collection to the model, the retriever can select relevant chunks.

### Source-Grounded Responses

Retrieved documents can be retained as supporting context and, in more advanced systems, exposed as citations or source references.

### Privacy-Friendly Local Architectures

A RAG pipeline can be designed around local models and local data when privacy requirements call for keeping documents on-device or within a controlled environment.

---

# Limitations of RAG

RAG does not automatically guarantee correct answers.

Possible problems include:

### Poor Chunking

Bad chunk boundaries can remove important context.

### Poor Embeddings

If the embedding model does not represent the query and documents effectively, retrieval quality can suffer.

### Wrong Retrieval

The retriever may return irrelevant chunks.

### Missing Information

If the correct information is not present in the knowledge base, retrieval cannot find it.

### Context Limitations

Too much retrieved information can make the prompt inefficient or exceed the model's usable context.

### LLM Hallucination

Even with retrieved context, the LLM can still generate incorrect information.

### Data Quality

Garbage or outdated source data can produce poor answers.

Therefore, a RAG system should be evaluated as a complete pipeline rather than assuming that adding retrieval automatically makes every answer correct.

---


# References

* Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* — original RAG research.
* AWS Prescriptive Guidance — *Understanding Retrieval Augmented Generation*.
* AWS Prescriptive Guidance — *Retrievers for RAG workflows*.
* AWS — *What is Retrieval-Augmented Generation?*