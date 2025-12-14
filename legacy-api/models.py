# models.py
# Pydantic 模型定義 - 用於 API 請求/回應的資料驗證

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


# ============================================================
# 書籍相關模型
# ============================================================

class BookBase(BaseModel):
    """書籍基本資料"""
    title: str = Field(..., description="書名", example="挪威的森林")
    author_id: int = Field(..., description="作者 ID", example=1)
    category_id: int = Field(..., description="分類 ID", example=1)
    isbn: str = Field(..., description="ISBN", example="978-957-13-5244-3")
    price: float = Field(..., description="價格", ge=0, example=380)
    stock: int = Field(0, description="庫存數量", ge=0, example=25)
    publish_date: Optional[str] = Field(None, description="出版日期", example="1987-09-04")
    description: Optional[str] = Field(None, description="書籍描述")


class BookCreate(BookBase):
    """新增書籍請求"""
    pass


class BookUpdate(BaseModel):
    """更新書籍請求（所有欄位都是可選的）"""
    title: Optional[str] = Field(None, description="書名")
    author_id: Optional[int] = Field(None, description="作者 ID")
    category_id: Optional[int] = Field(None, description="分類 ID")
    isbn: Optional[str] = Field(None, description="ISBN")
    price: Optional[float] = Field(None, description="價格", ge=0)
    stock: Optional[int] = Field(None, description="庫存數量", ge=0)
    publish_date: Optional[str] = Field(None, description="出版日期")
    description: Optional[str] = Field(None, description="書籍描述")


class BookResponse(BookBase):
    """書籍回應"""
    id: int = Field(..., description="書籍 ID")

    class Config:
        from_attributes = True


class BookWithDetails(BookResponse):
    """書籍詳細資訊（包含作者與分類名稱）"""
    author_name: Optional[str] = Field(None, description="作者名稱")
    category_name: Optional[str] = Field(None, description="分類名稱")


# ============================================================
# 庫存相關模型
# ============================================================

class StockUpdate(BaseModel):
    """庫存更新請求"""
    quantity_change: int = Field(
        ..., 
        description="庫存變動數量（正數增加，負數減少）",
        example=5
    )


# ============================================================
# 作者相關模型
# ============================================================

class AuthorBase(BaseModel):
    """作者基本資料"""
    name: str = Field(..., description="作者名稱", example="村上春樹")
    country: Optional[str] = Field(None, description="國籍", example="日本")
    bio: Optional[str] = Field(None, description="作者簡介")


class AuthorResponse(AuthorBase):
    """作者回應"""
    id: int = Field(..., description="作者 ID")

    class Config:
        from_attributes = True


class AuthorWithBooks(AuthorResponse):
    """作者資訊（包含其著作）"""
    books: list[BookResponse] = Field(default_factory=list, description="該作者的書籍")


# ============================================================
# 分類相關模型
# ============================================================

class CategoryBase(BaseModel):
    """分類基本資料"""
    name: str = Field(..., description="分類名稱", example="文學小說")
    description: Optional[str] = Field(None, description="分類描述")


class CategoryResponse(CategoryBase):
    """分類回應"""
    id: int = Field(..., description="分類 ID")

    class Config:
        from_attributes = True


class CategoryWithBooks(CategoryResponse):
    """分類資訊（包含該分類的書籍）"""
    books: list[BookResponse] = Field(default_factory=list, description="該分類的書籍")


# ============================================================
# 統計相關模型
# ============================================================

class LowStockBook(BaseModel):
    """低庫存書籍"""
    id: int
    title: str
    stock: int


class InventoryStats(BaseModel):
    """庫存統計"""
    total_titles: int = Field(..., description="書籍總種類數")
    total_stock: int = Field(..., description="總庫存數量")
    total_inventory_value: float = Field(..., description="庫存總價值")
    low_stock_count: int = Field(..., description="低庫存書籍數量")
    out_of_stock_count: int = Field(..., description="缺貨書籍數量")
    low_stock_books: list[LowStockBook] = Field(..., description="低庫存書籍清單")


# ============================================================
# 通用回應模型
# ============================================================

class MessageResponse(BaseModel):
    """通用訊息回應"""
    message: str = Field(..., description="訊息內容")
    success: bool = Field(True, description="是否成功")


class ErrorResponse(BaseModel):
    """錯誤回應"""
    detail: str = Field(..., description="錯誤詳情")
