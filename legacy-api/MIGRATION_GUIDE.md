# 🔄 從 REST API 遷移到 MCP Server 指南

本指南將說明如何將「書店庫存管理系統」REST API 轉換為 MCP Server，讓 AI 能夠直接與你的 API 互動。

---

## 為什麼要遷移到 MCP？

### REST API 的限制

```
┌─────────────┐      HTTP Request      ┌─────────────┐
│   Client    │ ───────────────────►   │  REST API   │
│  (前端/App) │ ◄───────────────────   │             │
└─────────────┘      JSON Response     └─────────────┘
```

- 需要人工撰寫 API 呼叫程式碼
- AI 無法直接理解和操作
- 需要額外的 API 文件

### MCP 的優勢

```
┌─────────────┐                                  ┌─────────────┐
│  AI Client  │ ◄─── Model Context Protocol ───► │ MCP Server  │
│ (Cursor/    │     (雙向通訊)                    │  (Tools/    │
│  Claude)    │                                  │  Resources) │
└─────────────┘                                  └─────────────┘
```

- AI 可以直接發現和呼叫工具
- 自動理解參數和用途
- 支援雙向通訊（包括 Sampling）

---

## 前置準備: 確保 REST API 正在運行

```bash
cd legacy-api
python app.py
```

確認可以訪問：

- API: http://localhost:8012
- OpenAPI JSON: http://localhost:8012/openapi.json

---

## 方法一：自動轉換（OpenAPI → MCP）

> **最快速的方式**：讓 FastMCP 自動從 OpenAPI 規格生成 MCP Server

### Step 1: 建立 MCP Server 檔案

在 `legacy-api` 資料夾中建立 `bookstore_mcp.py`：

```python
# bookstore_mcp.py
# 將書店 REST API 自動轉換為 MCP Server

import httpx
from fastmcp import FastMCP

# 1. 建立 HTTP Client 連接到 REST API
client = httpx.AsyncClient(base_url="http://localhost:8012")

# 2. 取得 OpenAPI 規格
openapi_spec = httpx.get("http://localhost:8012/openapi.json").json()

# 3. 自動轉換為 MCP Server
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="📚 書店庫存管理 MCP Server"
)

if __name__ == "__main__":
    mcp.run()
```

### Step 2: 運行 MCP Server

```bash
# 確保 REST API 正在運行（在另一個終端）
# python app.py

# 啟動 MCP Server
fastmcp dev bookstore_mcp.py
```

就這樣！所有 REST API 端點都會自動轉換為 MCP Tools。

---

## 方法二：手動遷移（推薦用於生產環境）

> **更好的 LLM 效能**：手動設計的 MCP Server 讓 AI 表現更好

### 建立 MCP Server

[bookstore_mcp_manual.py](bookstore_mcp_manual.py)

### 根據用途設定為不同模式

    - GET /books/{id} → MCP Resource
    - POST/PUT/DELETE → MCP Tools
    - 加入 Prompt Templates

### 運行 MCP Server

```bash
fastmcp dev bookstore_mcp_manual.py
```

---

## REST vs MCP 對照表

| REST API                  | MCP Server                         | 說明             |
| ------------------------- | ---------------------------------- | ---------------- |
| `GET /books`              | `@mcp.resource()` 或 `@mcp.tool()` | 讀取資料         |
| `GET /books/{id}`         | `@mcp.resource("uri/{id}")`        | 動態資源         |
| `GET /books/search?q=...` | `@mcp.tool()`                      | 有參數的查詢     |
| `POST /books`             | `@mcp.tool()`                      | 建立資源         |
| `PUT /books/{id}`         | `@mcp.tool()`                      | 更新資源         |
| `DELETE /books/{id}`      | `@mcp.tool()`                      | 刪除資源         |
| OpenAPI description       | Tool docstring                     | 告訴 AI 何時使用 |
| Query parameters          | Tool arguments                     | 函數參數         |
| JSON response             | 字串/結構化回傳                    | 回傳值           |

### 轉換原則

1. **讀取操作（無副作用）** → 優先使用 `Resource`
2. **需要參數的讀取** → 使用 `Resource Template` 或 `Tool`
3. **寫入操作（有副作用）** → 必須使用 `Tool`
4. **複雜業務邏輯** → 使用 `Tool` + 詳細 docstring

---

**你已經學會如何將傳統 REST API 轉換為 MCP Server！** 🎉
