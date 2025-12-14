# Demo MCP Server

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) Server 教學專案，使用 [FastMCP](https://gofastmcp.com/getting-started/welcome) 框架快速建立 AI Agent 可呼叫的工具。

## 專案結構

```
├── server.py              # 貨幣轉換 MCP Server（入門範例）
├── CHALLENGE_RAG.md       # 挑戰 1：實作 RAG 向量搜尋
├── CHALLENGE_SAMPLING.md  # 挑戰 2：實作 Sampling 功能
└── legacy-api/            # REST API 遷移至 MCP 範例
```

## Transport 轉變

SSE 是早期的臨時方案，有先天限制；Streamable HTTP 設計更符合實際使用。
SSE 不會馬上消失，但已被標記為過時（deprecated）。

### 從 SSE 遷移到 Streamable HTTP

**Step 1：修改 transport 參數**

```python
# 舊版 SSE（已棄用）
mcp.run(transport="sse")

# 新版 Streamable HTTP
mcp.run(transport="http")
```

**Step 2：更新 Client 連線 URL**

```
# SSE 端點
http://localhost:8080/sse

# Streamable HTTP 端點
http://localhost:8080/mcp
```
