# mock_db.py
# 模擬資料庫 - 書店庫存管理系統
# 這個檔案模擬了一個簡單的資料庫，所有資料都存在記憶體中

from datetime import date
from typing import Optional

# ============================================================
# 模擬資料
# ============================================================

# 作者資料
AUTHORS = {
    1: {
        "id": 1,
        "name": "村上春樹",
        "country": "日本",
        "bio": "日本當代著名作家，作品風格獨特，融合現實與超現實。"
    },
    2: {
        "id": 2,
        "name": "金庸",
        "country": "香港",
        "bio": "武俠小說泰斗，創作了多部膾炙人口的武俠經典。"
    },
    3: {
        "id": 3,
        "name": "J.K. Rowling",
        "country": "英國",
        "bio": "英國作家，以《哈利波特》系列聞名全球。"
    },
    4: {
        "id": 4,
        "name": "東野圭吾",
        "country": "日本",
        "bio": "日本推理小說作家，作品多次改編為影視作品。"
    },
    5: {
        "id": 5,
        "name": "侯文詠",
        "country": "台灣",
        "bio": "台灣作家、醫師，作品幽默風趣，深受讀者喜愛。"
    }
}

# 分類資料
CATEGORIES = {
    1: {"id": 1, "name": "文學小說", "description": "純文學與現代小說"},
    2: {"id": 2, "name": "武俠小說", "description": "武俠與奇幻類型小說"},
    3: {"id": 3, "name": "奇幻文學", "description": "魔法與奇幻世界的故事"},
    4: {"id": 4, "name": "推理懸疑", "description": "偵探推理與懸疑驚悚"},
    5: {"id": 5, "name": "散文隨筆", "description": "生活感悟與散文創作"}
}

# 書籍資料
BOOKS = {
    1: {
        "id": 1,
        "title": "挪威的森林",
        "author_id": 1,
        "category_id": 1,
        "isbn": "978-957-13-5244-3",
        "price": 380,
        "stock": 25,
        "publish_date": "1987-09-04",
        "description": "村上春樹最著名的長篇小說，描述青年渡邊徹的愛情故事。"
    },
    2: {
        "id": 2,
        "title": "1Q84",
        "author_id": 1,
        "category_id": 1,
        "isbn": "978-957-13-5100-2",
        "price": 450,
        "stock": 18,
        "publish_date": "2009-05-29",
        "description": "村上春樹的長篇巨作，交織現實與平行世界的故事。"
    },
    3: {
        "id": 3,
        "title": "射鵰英雄傳",
        "author_id": 2,
        "category_id": 2,
        "isbn": "978-957-33-1234-5",
        "price": 520,
        "stock": 30,
        "publish_date": "1957-01-01",
        "description": "金庸武俠經典，講述郭靖的成長與江湖恩怨。"
    },
    4: {
        "id": 4,
        "title": "神鵰俠侶",
        "author_id": 2,
        "category_id": 2,
        "isbn": "978-957-33-1235-2",
        "price": 550,
        "stock": 22,
        "publish_date": "1959-05-20",
        "description": "金庸武俠名作，楊過與小龍女的愛情傳奇。"
    },
    5: {
        "id": 5,
        "title": "哈利波特：神秘的魔法石",
        "author_id": 3,
        "category_id": 3,
        "isbn": "978-957-33-2001-1",
        "price": 320,
        "stock": 50,
        "publish_date": "1997-06-26",
        "description": "哈利波特系列第一集，開啟魔法世界的大門。"
    },
    6: {
        "id": 6,
        "title": "哈利波特：消失的密室",
        "author_id": 3,
        "category_id": 3,
        "isbn": "978-957-33-2002-8",
        "price": 350,
        "stock": 45,
        "publish_date": "1998-07-02",
        "description": "哈利波特系列第二集，霍格華茲的神秘事件。"
    },
    7: {
        "id": 7,
        "title": "嫌疑犯X的獻身",
        "author_id": 4,
        "category_id": 4,
        "isbn": "978-957-13-4521-6",
        "price": 300,
        "stock": 35,
        "publish_date": "2005-08-25",
        "description": "東野圭吾代表作，天才數學家的完美犯罪。"
    },
    8: {
        "id": 8,
        "title": "解憂雜貨店",
        "author_id": 4,
        "category_id": 1,
        "isbn": "978-957-13-5678-9",
        "price": 320,
        "stock": 40,
        "publish_date": "2012-03-28",
        "description": "東野圭吾溫馨之作，時空交錯的療癒故事。"
    },
    9: {
        "id": 9,
        "title": "白色巨塔",
        "author_id": 5,
        "category_id": 1,
        "isbn": "978-957-32-5432-1",
        "price": 380,
        "stock": 28,
        "publish_date": "1999-06-15",
        "description": "侯文詠醫療小說，揭露醫院體制的人性掙扎。"
    },
    10: {
        "id": 10,
        "title": "危險心靈",
        "author_id": 5,
        "category_id": 1,
        "isbn": "978-957-32-5433-8",
        "price": 350,
        "stock": 20,
        "publish_date": "2003-07-01",
        "description": "侯文詠教育小說，探討台灣教育體制的問題。"
    }
}

# 自動遞增 ID
_next_book_id = max(BOOKS.keys()) + 1
_next_author_id = max(AUTHORS.keys()) + 1
_next_category_id = max(CATEGORIES.keys()) + 1


# ============================================================
# 資料庫操作函數 - 書籍
# ============================================================

def get_all_books() -> list[dict]:
    """取得所有書籍"""
    return list(BOOKS.values())


def get_book_by_id(book_id: int) -> Optional[dict]:
    """根據 ID 取得書籍"""
    return BOOKS.get(book_id)


def search_books(
    keyword: Optional[str] = None,
    author_id: Optional[int] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None
) -> list[dict]:
    """搜尋書籍"""
    results = list(BOOKS.values())
    
    if keyword:
        keyword_lower = keyword.lower()
        results = [
            b for b in results
            if keyword_lower in b["title"].lower() 
            or keyword_lower in b.get("description", "").lower()
        ]
    
    if author_id:
        results = [b for b in results if b["author_id"] == author_id]
    
    if category_id:
        results = [b for b in results if b["category_id"] == category_id]
    
    if min_price is not None:
        results = [b for b in results if b["price"] >= min_price]
    
    if max_price is not None:
        results = [b for b in results if b["price"] <= max_price]
    
    if in_stock is not None:
        if in_stock:
            results = [b for b in results if b["stock"] > 0]
        else:
            results = [b for b in results if b["stock"] == 0]
    
    return results


def create_book(book_data: dict) -> dict:
    """新增書籍"""
    global _next_book_id
    book_id = _next_book_id
    _next_book_id += 1
    
    book = {
        "id": book_id,
        **book_data
    }
    BOOKS[book_id] = book
    return book


def update_book(book_id: int, book_data: dict) -> Optional[dict]:
    """更新書籍"""
    if book_id not in BOOKS:
        return None
    
    BOOKS[book_id].update(book_data)
    return BOOKS[book_id]


def delete_book(book_id: int) -> bool:
    """刪除書籍"""
    if book_id not in BOOKS:
        return False
    del BOOKS[book_id]
    return True


def update_stock(book_id: int, quantity_change: int) -> Optional[dict]:
    """更新庫存（正數增加，負數減少）"""
    if book_id not in BOOKS:
        return None
    
    new_stock = BOOKS[book_id]["stock"] + quantity_change
    if new_stock < 0:
        return None  # 庫存不足
    
    BOOKS[book_id]["stock"] = new_stock
    return BOOKS[book_id]


# ============================================================
# 資料庫操作函數 - 作者
# ============================================================

def get_all_authors() -> list[dict]:
    """取得所有作者"""
    return list(AUTHORS.values())


def get_author_by_id(author_id: int) -> Optional[dict]:
    """根據 ID 取得作者"""
    return AUTHORS.get(author_id)


def get_books_by_author(author_id: int) -> list[dict]:
    """取得特定作者的所有書籍"""
    return [b for b in BOOKS.values() if b["author_id"] == author_id]


# ============================================================
# 資料庫操作函數 - 分類
# ============================================================

def get_all_categories() -> list[dict]:
    """取得所有分類"""
    return list(CATEGORIES.values())


def get_category_by_id(category_id: int) -> Optional[dict]:
    """根據 ID 取得分類"""
    return CATEGORIES.get(category_id)


def get_books_by_category(category_id: int) -> list[dict]:
    """取得特定分類的所有書籍"""
    return [b for b in BOOKS.values() if b["category_id"] == category_id]


# ============================================================
# 統計函數
# ============================================================

def get_inventory_stats() -> dict:
    """取得庫存統計"""
    total_books = len(BOOKS)
    total_stock = sum(b["stock"] for b in BOOKS.values())
    total_value = sum(b["price"] * b["stock"] for b in BOOKS.values())
    low_stock_books = [b for b in BOOKS.values() if b["stock"] < 10]
    out_of_stock = [b for b in BOOKS.values() if b["stock"] == 0]
    
    return {
        "total_titles": total_books,
        "total_stock": total_stock,
        "total_inventory_value": total_value,
        "low_stock_count": len(low_stock_books),
        "out_of_stock_count": len(out_of_stock),
        "low_stock_books": [{"id": b["id"], "title": b["title"], "stock": b["stock"]} for b in low_stock_books]
    }
