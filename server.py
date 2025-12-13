from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Currency Converter Service")

# Tool
@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    貨幣轉換（使用固定匯率作為示範）。

    Args:
        amount: 金額
        from_currency: 來源貨幣（USD, TWD, JPY, EUR）
        to_currency: 目標貨幣（USD, TWD, JPY, EUR）

    Returns:
        轉換後的金額
    """
    # 示範用固定匯率（實際應用應使用即時匯率 API）
    rates = {
        "USD": 1.0,
        "TWD": 31.5,
        "JPY": 149.5,
        "EUR": 0.92
    }

    if from_currency not in rates or to_currency not in rates:
        raise ValueError(f"不支援的貨幣：{from_currency} 或 {to_currency}")
    
    amount_in_usd = amount / rates[from_currency]
    result = amount_in_usd * rates[to_currency]
    return f"{amount} {from_currency} = {result:.2f} {to_currency}"

# Resource
@mcp.resource("currency://rates/{currency}")
def currency_rates(currency: str) -> str:
    """提供特定貨幣的匯率資訊（相對於 USD）。"""
    rates = {
        "USD": 1.0,
        "TWD": 31.5,
        "JPY": 149.5,
        "EUR": 0.92
    }
    if currency in rates:
        return f"貨幣：{currency}\n匯率（相對於 USD）：{rates[currency]}\n更新時間：示範資料"
    else:
        raise ValueError(f"不支援的貨幣：{currency}")

# Prompt
@mcp.prompt()
def currency_converter_prompt(from_currency: str, to_currency: str) -> str:
    """貨幣轉換助手（附帶當前匯率資訊）"""
    return f"""你是一個專業的貨幣轉換助手。

當前任務：協助用戶將 {from_currency} 轉換為 {to_currency}

請提供：
1. 即時匯率資訊
2. 轉換計算
3. 匯率趨勢建議（如果相關）

使用 convert_currency 工具來執行實際轉換。
使用 currency://rates 資源來查詢匯率資料。"""


# Run the server
if __name__ == "__main__":
    mcp.run()