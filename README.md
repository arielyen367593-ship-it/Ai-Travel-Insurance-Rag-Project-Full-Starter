# Ai-Travel-Insurance-Rag-Project-Full-Starter
# AI Travel Insurance Agent

AI 旅平險專員 RAG 系統
使用 LangChain + FAISS + OpenAI 實現智慧保險問答

專案目標（對應報告第1-2頁）
- 建立文件檢索系統，讓民眾投保旅平險前能徹底了解保單內容
- 當作**專屬 AI 保險專員**，解答自己或親朋好友的所有疑問

旅平險特色挑戰（報告第3頁）
- 結構化＋非結構化混合（表格、除外責任、清單、法律術語）
- 語意歧義性（出發 vs 回程飛機延誤）
- 多層邏輯條件（特定國家＋住院超過3天 → 加成5%）

系統架構 - RAG 文件檢索系統（報告第4-5頁）
- 解決 LLM 幻覺與知識過時問題
- **可溯源性**：每句回答都會標註「根據國泰條款第12條第3項」
- 使用 **LangChain + FAISS + OpenAI text-embedding-3-large**

**支援保單**：
- 國泰
- 富邦
- 新光
（可輕鬆擴充其他公司）

---

## 🛠 AI 工具鏈整合與任務執行紀錄

| 任務                  | 使用 AI 工具              | 系統環境          | 輔助工具              |
|-----------------------|---------------------------|-------------------|-----------------------|
| PDF 解析與 Chunking   | ChatGPT-4o + Claude      | Windows + WSL2    | pdfplumber + LangChain |
| Embedding 與 Vector DB| Grok + NotebookLM        | Python 3.11       | FAISS + Chroma        |
| RAG Pipeline 開發     | Cursor + GitHub Copilot  | VS Code           | LangChain             |
| Streamlit 前端        | Grok                     | Streamlit Cloud   | VS Code               |
| 驗證分析              | NotebookLM（基準系統）   | Jupyter           | 手動 QA 評分          |

---

## 📋 系統完整設計流程

### 1. 資料收集
- 下載國泰、富邦、新光旅平險官方 PDF 保單
- 放入 `data/raw/` 資料夾

### 2. 資料處理與向量化
- Parsing → Cleaning → Semantic Chunking
- Embedding 後存入 FAISS Vector Database

### 3. RAG 檢索流程
- 使用者問題 → Embedding → 相似度檢索 Top-5 chunks
- 將 chunks 放入 Prompt → GPT-4o 生成答案 + Citation

### 4. 驗證分析
- 使用 **NotebookLM** 作為基準系統
- 製作 20 題標準測試 QA
- 比較「本系統」與「NotebookLM」在正確率、引用正確性、幻覺率的差異
- 提供詳細分析報告（見 `notebooks/validation.ipynb`）

**最終效能不重要，分析過程與改進建議才是重點！**

---

## 📁 專案目錄結構

```bash
Ai-Travel-Insurance-Rag-Project-Full-Starter/
├── data/                  # 保險 PDF（國泰、富邦、新光）
├── notebooks/             # 驗證與處理 Notebook
├── src/                   # RAG 核心程式碼
├── app/                   # Streamlit 前端
├── images/                # 報告截圖 + PDF 封面
├── requirements.txt
├── README.md
├── report.pdf             # 期末報告 PDF
└── .env.example
## AI 工具鏈整合與任務執行紀錄 (20%)

| 任務                  | 使用 AI 工具                  | 系統環境          | 輔助 IDE / 工具          |
|-----------------------|-------------------------------|-------------------|--------------------------|
| PDF 解析與資料收集    | ChatGPT-4o + Grok            | Windows 11        | VS Code + PyPDF         |
| Chunking 與 Embedding | HuggingFace + LangChain      | Python 3.10       | Jupyter Notebook        |
| 向量資料庫建立        | FAISS + sentence-transformers| 本地電腦          | Cursor + GitHub Copilot |
| RAG 問答系統開發      | Grok + Claude                | Streamlit         | VS Code                 |
| 驗證分析              | NotebookLM（基準系統）       | Jupyter           | 手動 QA 評分            |

 系統完整設計流程 (70%)

1. 資料收集
- 下載國泰、富邦、新光三家官方旅平險 PDF 保單，放入 `data/` 資料夾

2. 資料處理與向量化
- PDF Parsing（PyPDF）→ Text Cleaning → RecursiveCharacterTextSplitter (chunk_size=500, overlap=100)
- 使用 `sentence-transformers/all-MiniLM-L6-v2` 進行 Embedding
- 存入 FAISS 向量資料庫

#3. RAG 問答流程
- 使用者提問 → Embedding → FAISS 檢索 Top-6 → GPT-4o-mini 生成答案 + Citation

#4. 驗證分析（最重要！）
- 使用 **NotebookLM** 作為基準系統
- 製作 4 個測試問題（班機延誤、回程取消、酒醉受傷、海外住院）
- 比較結果見報告第 9 頁表格
- 驗證方式：手動檢查答案是否與保單條文一致 + 計算 Citation 正確率
- 結論：本系統在中文條文理解與 Citation 能力優於 NotebookLM，回答速度更快

最終效能不重要，分析過程與改進建議才是重點！
