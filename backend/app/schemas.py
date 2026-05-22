from pydantic import BaseModel
from datetime import date
from typing import Optional

# 1. Базовый класс
class TransactionBase(BaseModel):
    type: str          # 'income' или 'expense'
    amount: float
    currency: str      # 'BYN', 'USD', 'EUR', 'RUB'
    category: str
    date: date
    description: Optional[str] = None

# 2. Класс для создания транзакции (ИМЕННО ЕГО НЕ ВИДИТ СЕРВЕР)
class TransactionCreate(TransactionBase):
    pass

# 3. Класс ответа для транзакции
class TransactionResponse(TransactionBase):
    id: int
    telegram_user_id: int

    class Config:
        from_attributes = True

# 4. Класс для создания лимитов
class BudgetLimitCreate(BaseModel):
    category: str
    limit_amount: float
    currency: str

# 5. Класс ответа для лимитов
class BudgetLimitResponse(BudgetLimitCreate):
    id: int
    telegram_user_id: int

    class Config:
        from_attributes = True