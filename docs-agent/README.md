
## 🚧 Current Status: Early Implementation Stage

This repository contains an **initial version** of the system that implements the hierarchical retrieval flow described above. It leverages the open-source project [LangConnect-Client](https://github.com/teddynote-lab/LangConnect-Client) and will gradually integrate all components as **MCP server tools**.

### 🔧 Planned Pipeline Overview

The following steps represent the overall retrieval and generation process, with tools and libraries indicated for each stage:

### 1. Crawling URLs and Descriptions from llms.txt
 → Tool: Crawling4ai

### 2. Save extracted URLs and descriptions
→ Storage: Supabase database

### 3. Document List Retrieval
→ FAISS vector similarity search

### 4. URL Page Fetch
→ Tools: requests, BeautifulSoup

### 5. Context Filter (Compression)
→ FAISS vector similarity search

### 6. Final Answer Generation
