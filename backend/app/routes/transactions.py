from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Transaction, BudgetLimit
from app.schemas import TransactionCreate, TransactionResponse, BudgetLimitCreate, BudgetLimitResponse
from app.auth import verify_tg_init_data
from app.config import settings

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])

@router.post("", response_model=TransactionResponse)
def create_transaction(
    tx: TransactionCreate, 
    user_id: int = Depends(verify_tg_init_data), 
    db: Session = Depends(get_db)
):
    """Добавление новой операции (доход/расход)"""
    db_tx = Transaction(**tx.model_dump(), telegram_user_id=user_id)
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx

@router.get("", response_model=List[TransactionResponse])
def get_transactions(
    user_id: int = Depends(verify_tg_init_data), 
    db: Session = Depends(get_db)
):
    """Получение истории операций текущего пользователя"""
    return db.query(Transaction).filter(Transaction.telegram_user_id == user_id).order_by(Transaction.date.desc()).all()

@router.post("/limits", response_model=BudgetLimitResponse)
def set_limit(
    limit: BudgetLimitCreate, 
    user_id: int = Depends(verify_tg_init_data), 
    db: Session = Depends(get_db)
):
    """Установка или обновление лимита бюджета на категорию"""
    existing = db.query(BudgetLimit).filter(
        BudgetLimit.telegram_user_id == user_id, 
        BudgetLimit.category == limit.category,
        BudgetLimit.currency == limit.currency
    ).first()
    
    if existing:
        existing.limit_amount = limit.limit_amount
        db.commit()
        db.refresh(existing)
        return existing
        
    db_limit = BudgetLimit(**limit.model_dump(), telegram_user_id=user_id)
    db.add(db_limit)
    db.commit()
    db.refresh(db_limit)
    return db_limit

@router.post("/bot-add")
def create_transaction_from_bot(
    tx: TransactionCreate,
    x_bot_secret: str = Header(None),
    x_telegram_user_id: str = Header(None),
    db: Session = Depends(get_db)
):
    """Специальный закрытый эндпоинт для нашего Telegram-бота"""
    if not x_bot_secret or x_bot_secret != settings.BOT_TOKEN:
        raise HTTPException(status_code=403, detail="Доступ запрещен: неверный секрет бота")
    
    db_tx = Transaction(**tx.model_dump(), telegram_user_id=int(x_telegram_user_id))
    db.add(db_tx)
    db.commit()
    return {"status": "success", "id": db_tx.id}