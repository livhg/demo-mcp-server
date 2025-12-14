# bookstore_mcp_manual.py
# 手動設計版本：精心設計的 MCP Server，提供更好的 LLM 體驗
#
# 這個版本直接使用 mock_db，不需要啟動 REST API
# 適合生產環境，因為手動設計的 Tool 讓 AI 表現更好

from fastmcp import FastMCP
import mock_db

# ============================================================
# 初始化 MCP Server
# ============================================================

mcp = FastMCP(
    "📚 書店庫存管理 MCP Server",
    instructions="""你是書店庫存管理助手。

你可以幫助使用者：
- 🔍 搜尋和查詢書籍資訊
- 📦 管理庫存數量
- 👤 查看作者資訊
- 📂 瀏覽書籍分類
- 📊 取得庫存統計報告

請用親切專業的語氣協助使用者。"""
)


# ============================================================
# MCP Tools - 書籍相關
# ============================================================

@mcp.tool()
def search_books(
    keyword: str = "",
    author_id: int = None,
    category_id: int = None,
    min_price: float = None,
    max_price: float = None,
    in_stock: bool = None
) -> str:
    """
    搜尋書籍。
    
    根據多種條件搜尋書籍，包括關鍵字、作者、分類、價格範圍等。
    當使用者想找特定書籍或瀏覽書籍時使用此工具。
    
    Args:
        keyword: 搜尋關鍵字，會搜尋書名和描述
        author_id: 作者 ID（使用 list_authors 查看所有作者）
        category_id: 分類 ID（使用 list_categories 查看所有分類）
        min_price: 最低價格
        max_price: 最高價格
        in_stock: True 只顯示有庫存，False 只顯示缺貨
    
    Returns:
        符合條件的書籍清單
    """
    books = mock_db.search_books(
        keyword=keyword or None,
        author_id=author_id,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock
    )
    
    if not books:
        return "📭 找不到符合條件的書籍"
    
    result = f"📚 找到 {len(books)} 本書籍：\n"
    result += "-" * 40 + "\n"
    
    for book in books:
        author = mock_db.get_author_by_id(book["author_id"])
        category = mock_db.get_category_by_id(book["category_id"])
        
        stock_status = "✅" if book["stock"] > 0 else "❌缺貨"
        
        result += f"\n📖 [{book['id']}] {book['title']}\n"
        result += f"   作者：{author['name'] if author else '未知'}\n"
        result += f"   分類：{category['name'] if category else '未知'}\n"
        result += f"   價格：${book['price']} | 庫存：{book['stock']} {stock_status}\n"
    
    return result


@mcp.tool()
def get_book_detail(book_id: int) -> str:
    """
    取得書籍的完整詳細資訊。
    
    當使用者想了解特定書籍的詳細內容時使用。
    
    Args:
        book_id: 書籍 ID（可從 search_books 結果中取得）
    
    Returns:
        書籍的完整資訊
    """
    book = mock_db.get_book_by_id(book_id)
    if not book:
        return f"❌ 找不到 ID 為 {book_id} 的書籍"
    
    author = mock_db.get_author_by_id(book["author_id"])
    category = mock_db.get_category_by_id(book["category_id"])
    
    stock_status = "有庫存 ✅" if book["stock"] > 0 else "缺貨 ❌"
    
    return f"""📖 {book['title']}
{"=" * 40}

📝 基本資訊
   ISBN：{book['isbn']}
   作者：{author['name'] if author else '未知'} ({author['country'] if author else ''})
   分類：{category['name'] if category else '未知'}
   出版日期：{book['publish_date']}

💰 價格與庫存
   價格：${book['price']}
   庫存：{book['stock']} 本 ({stock_status})

📄 簡介
{book['description']}

👤 關於作者
{author['bio'] if author else '無作者資訊'}
"""


# ============================================================
# MCP Tools - 庫存管理
# ============================================================

@mcp.tool()
def update_stock(book_id: int, quantity_change: int) -> str:
    """
    更新書籍庫存數量。
    
    可以增加或減少庫存。正數表示進貨，負數表示出貨/銷售。
    
    Args:
        book_id: 書籍 ID
        quantity_change: 數量變動（正數增加，負數減少）
    
    Returns:
        更新結果
    
    Examples:
        - update_stock(1, 10)  # 書籍 ID 1 進貨 10 本
        - update_stock(1, -3)  # 書籍 ID 1 賣出 3 本
    """
    # 先取得書籍資訊
    book = mock_db.get_book_by_id(book_id)
    if not book:
        return f"❌ 錯誤：找不到 ID 為 {book_id} 的書籍"
    
    old_stock = book["stock"]
    
    # 更新庫存
    result = mock_db.update_stock(book_id, quantity_change)
    if result is None:
        return f"❌ 錯誤：庫存不足，無法減少 {abs(quantity_change)} 本（目前庫存：{old_stock}）"
    
    action = "📥 進貨" if quantity_change > 0 else "📤 出貨"
    
    return f"""✅ 庫存更新成功

📖 書籍：{book['title']}
{action}：{abs(quantity_change)} 本
原庫存：{old_stock} 本
現庫存：{result['stock']} 本
"""


@mcp.tool()
def get_inventory_report() -> str:
    """
    取得完整的庫存統計報告。
    
    當使用者詢問庫存狀況、統計資料、需要補貨的書籍時使用。
    
    Returns:
        詳細的庫存統計報告
    """
    stats = mock_db.get_inventory_stats()
    
    report = f"""📊 庫存統計報告
{"=" * 40}

📈 總覽
   書籍種類：{stats['total_titles']} 種
   總庫存量：{stats['total_stock']} 本
   庫存總值：${stats['total_inventory_value']:,.0f}

⚠️ 警示
   低庫存（<10本）：{stats['low_stock_count']} 種
   完全缺貨：{stats['out_of_stock_count']} 種
"""
    
    if stats['low_stock_books']:
        report += "\n🔔 需要補貨的書籍：\n"
        for book in stats['low_stock_books']:
            urgency = "🔴" if book['stock'] == 0 else "🟡"
            report += f"   {urgency} [{book['id']}] {book['title']} - 剩餘 {book['stock']} 本\n"
    else:
        report += "\n✅ 所有書籍庫存充足！\n"
    
    return report


# ============================================================
# MCP Tools - 作者與分類
# ============================================================

@mcp.tool()
def list_authors() -> str:
    """
    列出所有作者及其著作數量。
    
    當使用者想查看有哪些作者、或想根據作者搜尋書籍時使用。
    """
    authors = mock_db.get_all_authors()
    
    result = "👤 作者列表\n"
    result += "=" * 40 + "\n"
    
    for author in authors:
        books = mock_db.get_books_by_author(author["id"])
        result += f"\n[{author['id']}] {author['name']} ({author['country']})\n"
        result += f"    著作數量：{len(books)} 本\n"
        result += f"    簡介：{author['bio'][:50]}...\n"
    
    return result


@mcp.tool()
def list_categories() -> str:
    """
    列出所有書籍分類及各分類的書籍數量。
    
    當使用者想瀏覽分類、或想根據分類搜尋書籍時使用。
    """
    categories = mock_db.get_all_categories()
    
    result = "📂 書籍分類\n"
    result += "=" * 40 + "\n"
    
    for category in categories:
        books = mock_db.get_books_by_category(category["id"])
        result += f"\n[{category['id']}] {category['name']}\n"
        result += f"    {category['description']}\n"
        result += f"    書籍數量：{len(books)} 本\n"
    
    return result


@mcp.tool()
def get_author_books(author_id: int) -> str:
    """
    取得特定作者的所有書籍。
    
    Args:
        author_id: 作者 ID（使用 list_authors 查看所有作者）
    """
    author = mock_db.get_author_by_id(author_id)
    if not author:
        return f"❌ 找不到 ID 為 {author_id} 的作者"
    
    books = mock_db.get_books_by_author(author_id)
    
    result = f"👤 {author['name']} 的著作\n"
    result += "=" * 40 + "\n"
    result += f"國籍：{author['country']}\n"
    result += f"簡介：{author['bio']}\n\n"
    result += f"📚 著作列表（共 {len(books)} 本）：\n"
    
    for book in books:
        result += f"  [{book['id']}] {book['title']} - ${book['price']}\n"
    
    return result


# ============================================================
# MCP Resources - 靜態資源
# ============================================================

@mcp.resource("bookstore://catalog")
def get_full_catalog() -> str:
    """完整書籍目錄"""
    books = mock_db.get_all_books()
    
    result = "📚 書店完整目錄\n"
    result += "=" * 50 + "\n\n"
    
    # 按分類整理
    categories = mock_db.get_all_categories()
    for category in categories:
        category_books = [b for b in books if b["category_id"] == category["id"]]
        if category_books:
            result += f"【{category['name']}】\n"
            for book in category_books:
                author = mock_db.get_author_by_id(book["author_id"])
                result += f"  • {book['title']} - {author['name']} (${book['price']})\n"
            result += "\n"
    
    return result


@mcp.resource("bookstore://authors")
def get_authors_info() -> str:
    """所有作者資訊"""
    authors = mock_db.get_all_authors()
    result = "👤 作者資訊\n\n"
    for author in authors:
        result += f"## {author['name']} ({author['country']})\n"
        result += f"{author['bio']}\n\n"
    return result


# ============================================================
# MCP Prompts - 提示詞模板
# ============================================================

@mcp.prompt()
def book_recommendation(preference: str = "經典文學") -> str:
    """書籍推薦助手"""
    return f"""你現在是專業的書店店員，正在幫客人推薦書籍。

客人的偏好：{preference}

請按照以下步驟：
1. 使用 search_books 或 list_categories 找到相關書籍
2. 挑選 2-3 本最適合的書籍
3. 詳細介紹每本書的特色
4. 說明為什麼這些書適合客人

請用親切專業的語氣回應。"""


@mcp.prompt()
def inventory_check() -> str:
    """庫存盤點助手"""
    return """你現在是書店的庫存管理員，正在進行庫存盤點。

請執行以下步驟：
1. 使用 get_inventory_report 取得庫存統計
2. 分析需要補貨的書籍
3. 提供具體的補貨建議（建議補貨數量）
4. 總結庫存健康狀況

請以專業的報告格式呈現。"""


@mcp.prompt()
def author_spotlight(author_name: str = "村上春樹") -> str:
    """作者特輯"""
    return f"""請為「{author_name}」製作一個作者特輯。

步驟：
1. 使用 list_authors 找到該作者的 ID
2. 使用 get_author_books 取得其所有著作
3. 為每本書使用 get_book_detail 取得詳細資訊
4. 撰寫一篇介紹該作者及其作品的文章

請用生動有趣的方式介紹。"""


# ============================================================
# 主程式
# ============================================================

if __name__ == "__main__":
    mcp.run()
