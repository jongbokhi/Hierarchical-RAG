# 🧠 Hierarchical RAG for Web Documents with MCP

## 🧩 Problem Scenario: Real-World Challenges of Web Document RAG

When building a Retrieval-Augmented Generation (RAG) system that crawls web documents, stores them in a VectorDB, and uses them for answering user queries, the following challenges emerge:

1. **Web documents are frequently updated**  
   → Periodically refreshing the entire VectorDB is **unrealistic** in terms of **cost and time**.

2. **Web documents are often large**  
   → A single page may contain multiple URLs, requiring recursive crawling. This may result in **context window overflow**.

3. **VectorDB-based retrieval alone cannot guarantee freshness or relevance**  
   → This can lead to **inaccurate answers** based on outdated or irrelevant documents.

---

## ✅ Solution: Hierarchical Retrieval and Generation with MCP

To tackle these challenges, we propose a **Hierarchical Retrieval and Generation** structure, particularly suited to the **MCP server architecture**.

### 🧱 Stage 1: Document List Retrieval

- Store a file called `llms.txt` in the VectorDB.
  - Each chunk contains:  
    **`[URL] + [Description]`**
  - Embedding is performed on these chunks.

- Upon receiving a query:
  - Perform a **vector search** over `llms.txt` to return the **most relevant URL(s)**.

- ✅ Benefits:
  - Filters out only relevant documents.
  - Avoids context overflow.
  - Provides fast and accurate results.

> 💡 _If `llms.txt` does not exist, manually create it using URLs and their descriptions._

---

### 🌐 Stage 2: URL Page Fetch

- Fetch the actual contents of the selected URLs **in real time**.

- ✅ Benefits:
  - The VectorDB only stores summary-level information → **efficient storage**.
  - The full document is fetched when needed → **ensures freshness**.

---

### ✂️ Stage 3: Context Filter (Compression)

- Fetched pages may contain **irrelevant information**.

- Apply a Context Filter to:
  - Extract only the sentences **directly related** to the query, or
  - **Summarize** the content before sending it to the LLM.

- ✅ Benefits:
  - Ensures **concise, relevant context**.
  - Improves **response accuracy**.

---

## 🔄 End-to-End Call Flow in MCP

The MCP server should follow this **fixed call sequence**:

Document List Retrieval
↓
URL Page Fetch
↓
Context Filter (Compression)
↓
Final Answer Generation


---

## ✅ Conclusion

RAG systems that rely on frequently updated web documents face major limitations when using VectorDB alone. The key solution lies in a **hierarchical call structure**:

> **Document List → Real-Time Fetch → Context Filtering**

This approach ensures:
- High relevance  
- Up-to-date content  
- Accurate responses  

Clearly separating the roles of each stage in the MCP server is crucial for reliability and scalability.

---

Feel free to contribute, raise issues, or fork this concept for your own use! 🚀



