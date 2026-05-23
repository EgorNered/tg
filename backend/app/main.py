import os
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Finance Tracker API",
    description="Backend for Telegram WebApp Wallet",
    version="1.0.0"
)

# =================================================================
# [КРИТИЧЕСКИ ВАЖНО] НАСТРОЙКА CORS МИДЛВАРЕ
# Она должна идти СРАЗУ после создания app и ДО подключения роутеров!
# =================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает запросы с любых доменов (включая Netlify)
    allow_credentials=True,
    allow_methods=["*"],  # Нативно обрабатывает OPTIONS, POST, GET, PUT, DELETE
    allow_headers=["*"],  # Принимает любые заголовки от фронтенда (Authorization, Content-Type и т.д.)
)

# Схемы данных Pydantic
class TransactionBase(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    type: str  # "income" или "expense"

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Базовый роутер для проверки статуса
@app.get("/")
async def root():
    return {"status": "ok", "message": "API is running smoothly", "timestamp": datetime.now()}

# Эндпоинты для транзакций (примерная структура)
@app.post("/api/transactions", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate):
    # Здесь твоя логика сохранения в БД (sqlite / sqlalchemy)
    # Пример возвращаемого ответа:
    return {
        "id": 1,
        "user_id: ": 12345678,
        "amount": transaction.amount,
        "category": transaction.category,
        "description": transaction.description,
        "type": transaction.type,
        "created_at": datetime.now()
    }

@app.get("/api/analytics/summary")
async def get_analytics_summary():
    # Эндпоинт аналитики, на котором падал OPTIONS
    return {
        "total_income": 0.0,
        "total_expense": 0.0,
        "balance": 0.0,
        "currency": "BYN"
    }

if __name__ == "__main__":
    import uvicorn
    # Railway автоматически передает порт через переменную окружения PORT
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main.py:app", host="0.0.0.0", port=port, reload=True)