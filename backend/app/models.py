from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(Integer, index=True, nullable=False)
    type = Column(String, nullable=False)         # 'income' (доход) или 'expense' (расход)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)     # 'BYN', 'USD', 'EUR', 'RUB'
    category = Column(String, nullable=False)     # 'еда', 'транспорт' и т.д.
    date = Column(Date, nullable=False)
    description = Column(String, nullable=True)   # Комментарий к платежу

class BudgetLimit(Base):
    __tablename__ = "budget_limits"

    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(Integer, index=True, nullable=False)
    category = Column(String, nullable=False)
    limit_amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)