# 挑戰：實作 MCP Sampling

## 目前進度 ✅

恭喜！你已經完成了：
- 建立第一個 MCP Server
- 實作 RAG 向量搜尋功能

現在讓我們進入 Sampling 挑戰！🚀

---

## 什麼是 Sampling？🤔

在之前的挑戰中，都是 **AI 呼叫 Server 的工具**。但 Sampling 讓我們可以反過來：

> **Server 請求 AI 幫忙生成內容！**

這開啟了許多可能性：
- 讓 Server 請求 AI 總結搜尋結果
- 讓 Server 請求 AI 翻譯內容
- 多步驟工作流程中的 AI 輔助
- 自動化內容生成管線

```
┌─────────────────┐         ┌─────────────────┐
│                 │  Tool   │                 │
│   AI Client     │ ──────► │   MCP Server    │
│  (Cursor/Claude)│         │                 │
│                 │ ◄────── │                 │
│                 │ Sampling│                 │
└─────────────────┘         └─────────────────┘
```

---

## 挑戰目標 🎯

實作一個具備 **Sampling** 功能的 MCP Server，讓 Server 可以請求 AI 幫忙：
1. 總結新聞文章
2. 翻譯內容
3. 生成智慧回應

---

## Step 1: 建立 Sampling Server

創建一個新檔案 `sampling_server.py`：

```python
# sampling_server.py
from fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent

# 1. 初始化 MCP Server（啟用 sampling）
mcp = FastMCP("Sampling Demo Server", host="localhost", port=8080)

# 模擬的新聞資料庫
news_database = {
    "tech": """
    OpenAI 今日宣布推出 GPT-5，這是其最新一代的大型語言模型。
    新模型在推理能力、多語言支援和程式碼生成方面都有顯著提升。
    CEO Sam Altman 表示，這標誌著 AI 發展的重要里程碑。
    該模型已開始向企業用戶開放測試。
    """,
    "sports": """
    世界杯足球賽昨晚結束了精彩的八強賽。
    法國隊以 2-1 擊敗英格蘭隊，晉級四強。
    比賽在加時賽中由 Mbappé 攻入致勝球。
    這是法國隊連續第二屆世界杯進入四強。
    """,
    "business": """
    台積電宣布將在日本熊本縣建設第三座晶圓廠。
    預計投資金額超過 200 億美元，將創造超過 3000 個就業機會。
    新廠預計於 2027 年開始量產，主要生產 3 奈米製程晶片。
    這是台積電海外擴張計畫的重要一步。
    """
}


# 2. 定義工具 - 使用 Sampling 來總結新聞
@mcp.tool()
async def summarize_news(category: str, language: str = "繁體中文") -> str:
    """
    取得指定類別的新聞並使用 AI 生成摘要。
    
    Args:
        category: 新聞類別 (tech, sports, business)
        language: 輸出語言 (繁體中文, English, 日本語)
    
    Returns:
        AI 生成的新聞摘要
    """
    if category not in news_database:
        return f"找不到類別：{category}。可用類別：tech, sports, business"
    
    news_content = news_database[category]
    
    # 🔥 這裡使用 Sampling - 請求 AI 幫忙總結！
    ctx = mcp.get_context()
    
    result = await ctx.sample(
        f"""請將以下新聞內容總結為 2-3 句話的精簡摘要。
使用 {language} 輸出。

新聞內容：
{news_content}

請只輸出摘要，不要加入任何額外說明。""",
        max_tokens=200
    )
    
    return f"📰 {category.upper()} 新聞摘要：\n\n{result.text}"


# 3. 定義工具 - 使用 Sampling 來翻譯
@mcp.tool()
async def smart_translate(text: str, target_language: str) -> str:
    """
    使用 AI 進行智慧翻譯（保留語氣和風格）。
    
    Args:
        text: 要翻譯的文字
        target_language: 目標語言 (English, 日本語, 한국어, 繁體中文)
    
    Returns:
        翻譯後的文字
    """
    ctx = mcp.get_context()
    
    # 使用 Sampling 請求 AI 翻譯
    result = await ctx.sample(
        f"""請將以下文字翻譯成 {target_language}。
保持原文的語氣和風格，進行自然的翻譯而非逐字翻譯。

原文：
{text}

請只輸出翻譯結果，不要加入任何說明。""",
        max_tokens=500
    )
    
    return f"🌐 翻譯結果 ({target_language})：\n\n{result.text}"


# 4. 定義工具 - 使用 Sampling 生成回應建議
@mcp.tool()
async def generate_reply_suggestions(message: str, tone: str = "professional") -> str:
    """
    根據收到的訊息，使用 AI 生成多個回覆建議。
    
    Args:
        message: 收到的訊息內容
        tone: 回覆語氣 (professional, friendly, formal, casual)
    
    Returns:
        三個不同的回覆建議
    """
    ctx = mcp.get_context()
    
    result = await ctx.sample(
        f"""你收到了以下訊息，請生成 3 個不同的回覆建議。
使用 {tone} 的語氣。

收到的訊息：
「{message}」

請以以下格式輸出：
1. [第一個回覆建議]
2. [第二個回覆建議]  
3. [第三個回覆建議]""",
        max_tokens=400
    )
    
    return f"💬 回覆建議（{tone} 語氣）：\n\n{result.text}"


# 啟動 Server
if __name__ == "__main__":
    mcp.run(transport="sse")
```

---

## Step 2: 運行 Sampling Server

確保虛擬環境已啟動，然後執行：

```bash
python sampling_server.py
```

你應該會看到：
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8080
```

---

## Step 3: 測試 Sampling 功能 🧪

### 使用 MCP Inspector

1. **開啟新終端**，啟動 Inspector：
```bash
npx @modelcontextprotocol/inspector
```

2. **連接到 Server**：
   - 選擇 **SSE** 連接方式
   - 輸入 URL：`http://localhost:8080/sse`
   - 點擊 **Connect**

3. **測試工具**：

| 工具 | 測試參數 | 預期結果 |
|------|----------|----------|
| `summarize_news` | category: "tech" | AI 生成的科技新聞摘要 |
| `smart_translate` | text: "你好世界", target_language: "English" | 翻譯結果 |
| `generate_reply_suggestions` | message: "明天的會議可以改期嗎？" | 3 個回覆建議 |

---
