# 挑戰：實作 RAG MCP Server

## 目前進度 ✅

恭喜！你已經完成了：
- 建立第一個 MCP Server
- 成功運行過基礎的 `server.py`

現在讓我們進入下一個挑戰！🚀

---

## 挑戰目標 🎯

實作一個具備 **RAG (Retrieval-Augmented Generation)** 功能的 MCP Server，讓 AI Agent 能夠從本地向量資料庫搜尋相關知識。

---

## Step 1: 安裝所需套件

使用 uv 安裝 txtai（本地向量資料庫）：

```bash
uv pip install txtai
```

> 💡 **什麼是 txtai？**  
> txtai 是一個輕量級的語義搜尋引擎，可以在本地建立向量資料庫，無需外部服務。

---

## Step 2: 修改 server.py

將 `server.py` 的內容替換為以下程式碼：

```python
# server.py
from fastmcp import FastMCP
from txtai import Embeddings

# 1. 初始化 MCP Server
mcp = FastMCP("My Local Vector DB", host="localhost", port=8080)

# 2. 初始化本地向量資料庫
embeddings = Embeddings()

# 儲存原始文檔（方便後續檢索）
documents = [
    "MCP 是一個開放的通訊協定",
    "Google Gemini 是強大的多模態模型",
    "VS Code 支援 MCP"
]

# 塞一點假資料 (實際應用這裡應該是讀 PDF/MD)
# txtai 格式: [(id, text, metadata), ...]
data = [(i, doc, None) for i, doc in enumerate(documents)]
embeddings.index(data)

# 3. 定義工具 (Tool) - 這就是 Agent 會看到的「技能」
@mcp.tool()
def search_knowledge_base(query: str) -> str:
    """
    從本地向量資料庫搜尋相關知識。
    當使用者問到技術名詞或定義時，請務必使用此工具。
    """
    # txtai 搜尋，返回 [(id, score), ...]
    results = embeddings.search(query, 2)
    
    # 格式化結果
    response = []
    for doc_id, score in results:
        response.append(f"{documents[doc_id]} (相關度: {score:.3f})")
    
    return "\n".join(response)

# 4. 啟動 Server (SSE 模式)
if __name__ == "__main__":
    mcp.run(transport="sse")  # 預設跑在 http://localhost:8080
```

---

## Step 3: 運行你的 RAG Server

確保虛擬環境已啟動（提示符顯示 `(mcp_env)`），然後執行：

```bash
python server.py
```

你應該會看到類似的輸出：
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8080
```

---

## 自訂配置 ⚙️

### 修改 Port

如果 8080 埠號已被佔用，你可以在初始化 FastMCP 時修改：

```python
mcp = FastMCP("My Local Vector DB", host="localhost", port=8888)
```

### 擴展知識庫

將 `documents` 列表替換為你自己的資料：

```python
documents = [
    "你的知識內容 1",
    "你的知識內容 2",
    "你的知識內容 3"
]
```

> 💡 **進階提示：** 實際應用中，這裡可以讀取 PDF、Markdown 或其他文檔格式！

---

## 測試你的 Server 🧪

### 方法 1：使用 MCP Inspector（推薦）

**步驟 1：** 在終端啟動 Server
```bash
python server.py
```

你應該會看到：
```
INFO:     Uvicorn running on http://localhost:8080
```

**步驟 2：** 開啟新終端，啟動 Inspector
```bash
npx @modelcontextprotocol/inspector
```

這會在瀏覽器中打開 Inspector Web UI

**步驟 3：** 在 Inspector 界面中連接到你的 Server

選擇連接方式：
- 點擊 **SSE** 選項
- 輸入 Server URL：`http://localhost:8080/sse`
- 點擊 **Connect** 按鈕

**步驟 4：** 測試工具

連接成功後，你應該能看到 `search_knowledge_base` 工具。試試看：
- 輸入查詢：「MCP 是什麼」
- 輸入查詢：「Gemini」
- 觀察搜尋結果和相關度分數

### 方法 2：使用 curl 快速驗證

```bash
curl http://localhost:8080/sse
```

成功的話會看到：
```
event: endpoint
data: /messages/?session_id=...
```

---

## 理解程式碼架構 📚

### 核心概念：

1. **向量資料庫 (Vector Database)**  
   - 將文字轉換為向量（數字表示）
   - 支援語義搜尋（不只是關鍵字匹配）

2. **MCP Tool**  
   - `@mcp.tool()` 裝飾器定義一個工具
   - AI Agent 可以主動呼叫這個工具
   - 工具的 docstring 會告訴 Agent 什麼時候該使用它

3. **SSE Transport**  
   - Server-Sent Events 傳輸模式
   - 適合本地開發和測試

---
