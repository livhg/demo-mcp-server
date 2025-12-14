# app.py
# 書店庫存管理系統 - REST API
# 這是一個「舊時代的 API」範例，展示傳統 REST 架構
# 未來將作為遷移到 MCP Server 的對照範例

from fastapi import FastAPI, HTTPException, Query
from fastapi.openapi.utils import get_openapi
from typing import Optional

from models import (
    BookCreate, BookUpdate, BookResponse, BookWithDetails,
    StockUpdate,
    AuthorResponse, AuthorWithBooks,
    CategoryResponse, CategoryWithBooks,
    InventoryStats, MessageResponse, ErrorResponse
)
import mock_db

# ============================================================
# 初始化 FastAPI 應用
# ============================================================

app = FastAPI(
    title="📚 書店庫存管理系統",
    description="""
## 書店庫存管理 REST API

這是一個傳統的 REST API 範例，用於管理書店的庫存系統。

### 功能特色
- 📖 書籍管理（CRUD 操作）
- 👤 作者資訊查詢
- 📂 分類瀏覽
- 📊 庫存統計

### 技術說明
這是一個「舊時代的 API」架構，使用 FastAPI + OpenAPI 規格。
未來將作為遷移到 MCP Server 的對照範例。

---
**Demo 專案 - 資料存放於記憶體中，重啟後會重置**
    """,
    version="1.0.0",
    contact={
        "name": "MCP Demo Project",
    },
    license_info={
        "name": "MIT",
    }
)


# ============================================================
# 書籍 API 端點
# ============================================================

@app.get(
    "/books",
    response_model=list[BookWithDetails],
    tags=["📖 書籍"],
    summary="取得所有書籍",
    description="取得書店中所有書籍的清單，包含作者與分類資訊"
)
def get_books():
    """取得所有書籍清單"""
    books = mock_db.get_all_books()
    return _enrich_books(books)


@app.get(
    "/books/search",
    response_model=list[BookWithDetails],
    tags=["📖 書籍"],
    summary="搜尋書籍",
    description="根據多種條件搜尋書籍"
)
def search_books(
    q: Optional[str] = Query(None, description="搜尋關鍵字（搜尋書名與描述）"),
    author_id: Optional[int] = Query(None, description="作者 ID"),
    category_id: Optional[int] = Query(None, description="分類 ID"),
    min_price: Optional[float] = Query(None, description="最低價格", ge=0),
    max_price: Optional[float] = Query(None, description="最高價格", ge=0),
    in_stock: Optional[bool] = Query(None, description="是否有庫存")
):
    """根據條件搜尋書籍"""
    books = mock_db.search_books(
        keyword=q,
        author_id=author_id,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock
    )
    return _enrich_books(books)


@app.get(
    "/books/{book_id}",
    response_model=BookWithDetails,
    tags=["📖 書籍"],
    summary="取得特定書籍",
    description="根據 ID 取得書籍詳細資訊",
    responses={404: {"model": ErrorResponse, "description": "書籍不存在"}}
)
def get_book(book_id: int):
    """根據 ID 取得書籍"""
    book = mock_db.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"找不到 ID 為 {book_id} 的書籍")
    return _enrich_book(book)


@app.post(
    "/books",
    response_model=BookWithDetails,
    status_code=201,
    tags=["📖 書籍"],
    summary="新增書籍",
    description="新增一本書籍到庫存中"
)
def create_book(book: BookCreate):
    """新增書籍"""
    # 驗證作者存在
    if not mock_db.get_author_by_id(book.author_id):
        raise HTTPException(status_code=400, detail=f"作者 ID {book.author_id} 不存在")
    
    # 驗證分類存在
    if not mock_db.get_category_by_id(book.category_id):
        raise HTTPException(status_code=400, detail=f"分類 ID {book.category_id} 不存在")
    
    new_book = mock_db.create_book(book.model_dump())
    return _enrich_book(new_book)


@app.put(
    "/books/{book_id}",
    response_model=BookWithDetails,
    tags=["📖 書籍"],
    summary="更新書籍",
    description="更新書籍資訊",
    responses={404: {"model": ErrorResponse, "description": "書籍不存在"}}
)
def update_book(book_id: int, book: BookUpdate):
    """更新書籍資訊"""
    # 驗證書籍存在
    existing = mock_db.get_book_by_id(book_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"找不到 ID 為 {book_id} 的書籍")
    
    # 驗證作者存在（如果有更新）
    if book.author_id and not mock_db.get_author_by_id(book.author_id):
        raise HTTPException(status_code=400, detail=f"作者 ID {book.author_id} 不存在")
    
    # 驗證分類存在（如果有更新）
    if book.category_id and not mock_db.get_category_by_id(book.category_id):
        raise HTTPException(status_code=400, detail=f"分類 ID {book.category_id} 不存在")
    
    # 只更新有值的欄位
    update_data = {k: v for k, v in book.model_dump().items() if v is not None}
    updated = mock_db.update_book(book_id, update_data)
    return _enrich_book(updated)


@app.delete(
    "/books/{book_id}",
    response_model=MessageResponse,
    tags=["📖 書籍"],
    summary="刪除書籍",
    description="從庫存中刪除書籍",
    responses={404: {"model": ErrorResponse, "description": "書籍不存在"}}
)
def delete_book(book_id: int):
    """刪除書籍"""
    if not mock_db.delete_book(book_id):
        raise HTTPException(status_code=404, detail=f"找不到 ID 為 {book_id} 的書籍")
    return MessageResponse(message=f"書籍 ID {book_id} 已成功刪除", success=True)


# ============================================================
# 庫存 API 端點
# ============================================================

@app.patch(
    "/books/{book_id}/stock",
    response_model=BookWithDetails,
    tags=["📦 庫存"],
    summary="更新庫存",
    description="增加或減少書籍庫存數量",
    responses={
        404: {"model": ErrorResponse, "description": "書籍不存在"},
        400: {"model": ErrorResponse, "description": "庫存不足"}
    }
)
def update_stock(book_id: int, stock_update: StockUpdate):
    """更新書籍庫存"""
    result = mock_db.update_stock(book_id, stock_update.quantity_change)
    if result is None:
        book = mock_db.get_book_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail=f"找不到 ID 為 {book_id} 的書籍")
        raise HTTPException(status_code=400, detail="庫存不足，無法減少")
    return _enrich_book(result)


@app.get(
    "/inventory/stats",
    response_model=InventoryStats,
    tags=["📦 庫存"],
    summary="庫存統計",
    description="取得整體庫存統計資訊"
)
def get_inventory_stats():
    """取得庫存統計"""
    return mock_db.get_inventory_stats()


# ============================================================
# 作者 API 端點
# ============================================================

@app.get(
    "/authors",
    response_model=list[AuthorResponse],
    tags=["👤 作者"],
    summary="取得所有作者",
    description="取得所有作者清單"
)
def get_authors():
    """取得所有作者"""
    return mock_db.get_all_authors()


@app.get(
    "/authors/{author_id}",
    response_model=AuthorWithBooks,
    tags=["👤 作者"],
    summary="取得作者詳情",
    description="取得作者資訊及其所有著作",
    responses={404: {"model": ErrorResponse, "description": "作者不存在"}}
)
def get_author(author_id: int):
    """取得作者及其著作"""
    author = mock_db.get_author_by_id(author_id)
    if not author:
        raise HTTPException(status_code=404, detail=f"找不到 ID 為 {author_id} 的作者")
    
    books = mock_db.get_books_by_author(author_id)
    return {**author, "books": books}


# ============================================================
# 分類 API 端點
# ============================================================

@app.get(
    "/categories",
    response_model=list[CategoryResponse],
    tags=["📂 分類"],
    summary="取得所有分類",
    description="取得所有書籍分類"
)
def get_categories():
    """取得所有分類"""
    return mock_db.get_all_categories()


@app.get(
    "/categories/{category_id}",
    response_model=CategoryWithBooks,
    tags=["📂 分類"],
    summary="取得分類詳情",
    description="取得分類資訊及該分類下的所有書籍",
    responses={404: {"model": ErrorResponse, "description": "分類不存在"}}
)
def get_category(category_id: int):
    """取得分類及其書籍"""
    category = mock_db.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail=f"找不到 ID 為 {category_id} 的分類")
    
    books = mock_db.get_books_by_category(category_id)
    return {**category, "books": books}


# ============================================================
# 輔助函數
# ============================================================

def _enrich_book(book: dict) -> dict:
    """為書籍加入作者名稱與分類名稱"""
    author = mock_db.get_author_by_id(book["author_id"])
    category = mock_db.get_category_by_id(book["category_id"])
    return {
        **book,
        "author_name": author["name"] if author else None,
        "category_name": category["name"] if category else None
    }


def _enrich_books(books: list[dict]) -> list[dict]:
    """為多本書籍加入作者名稱與分類名稱"""
    return [_enrich_book(book) for book in books]


# ============================================================
# 健康檢查
# ============================================================

@app.get(
    "/health",
    tags=["🔧 系統"],
    summary="健康檢查",
    description="檢查 API 服務狀態"
)
def health_check():
    """健康檢查端點"""
    return {
        "status": "healthy",
        "service": "Bookstore Inventory API",
        "version": "1.0.0"
    }


# ============================================================
# 主程式入口
# ============================================================

if __name__ == "__main__":
    import uvicorn
    print("🚀 啟動書店庫存管理系統 API...")
    print("📖 API 文件: http://localhost:8012/docs")
    print("📋 ReDoc 文件: http://localhost:8012/redoc")
    print("📄 OpenAPI JSON: http://localhost:8012/openapi.json")
    uvicorn.run(app, host="0.0.0.0", port=8012)
