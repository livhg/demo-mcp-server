# 📚 書店庫存管理系統 - Legacy REST API

這是一個「舊時代的 API」範例，展示傳統 REST 架構。
包含完整的 MCP Server 遷移範例，展示如何將傳統 API 轉換為 AI 可呼叫的工具。

## 🎯 專案目的

這個 API 模擬了一個真實的書店庫存管理系統，包含：

- 書籍管理（CRUD）
- 作者資訊查詢
- 分類瀏覽
- 庫存統計

## REST API (舊架構)

### 1. 安裝依賴

```bash
# 使用 pip
pip install -r requirements.txt

# 或使用 uv（推薦）
uv pip install -r requirements.txt
```

### 2. 啟動 REST API

```bash
python app.py
```

服務啟動後會在 `http://localhost:8012` 運行

### 3. 查看 API 文件

- **Swagger UI**: http://localhost:8012/docs
- **ReDoc**: http://localhost:8012/redoc
- **OpenAPI JSON**: http://localhost:8012/openapi.json

---

## 遷移到 MCP Server

詳細說明請參考 👉 **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)**

---

## 📖 API 端點

### 書籍 (Books)

| 方法   | 端點            | 說明         |
| ------ | --------------- | ------------ |
| GET    | `/books`        | 取得所有書籍 |
| GET    | `/books/search` | 搜尋書籍     |
| GET    | `/books/{id}`   | 取得特定書籍 |
| POST   | `/books`        | 新增書籍     |
| PUT    | `/books/{id}`   | 更新書籍     |
| DELETE | `/books/{id}`   | 刪除書籍     |

### 庫存 (Inventory)

| 方法  | 端點                | 說明     |
| ----- | ------------------- | -------- |
| PATCH | `/books/{id}/stock` | 更新庫存 |
| GET   | `/inventory/stats`  | 庫存統計 |

### 作者 (Authors)

| 方法 | 端點            | 說明               |
| ---- | --------------- | ------------------ |
| GET  | `/authors`      | 取得所有作者       |
| GET  | `/authors/{id}` | 取得作者（含著作） |

### 分類 (Categories)

| 方法 | 端點               | 說明               |
| ---- | ------------------ | ------------------ |
| GET  | `/categories`      | 取得所有分類       |
| GET  | `/categories/{id}` | 取得分類（含書籍） |

---

## 🔧 技術棧

- **FastAPI** - 現代 Python Web 框架
- **Pydantic** - 資料驗證
- **Uvicorn** - ASGI 伺服器
- **OpenAPI 3.0** - API 規格
- **FastMCP** - MCP Server 框架

## 📝 注意事項

- 這是 Demo 專案，資料存放於記憶體中
- 重啟服務後資料會重置
- 不需要外部資料庫

---

## 🎓 學習路徑

1. **REST API** (app.py) → 了解傳統 HTTP 端點
2. **自動轉換** (bookstore_mcp_auto.py) → 快速體驗 MCP
3. **手動設計** (bookstore_mcp_manual.py) → 最佳 LLM 體驗
4. **遷移指南** (MIGRATION_GUIDE.md) → 深入理解轉換過程
