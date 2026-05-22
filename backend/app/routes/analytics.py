from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

# Наши абсолютные импорты
from app.database import get_db
from app.models import Transaction, BudgetLimit
from app.auth import verify_tg_init_data

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

# ... далее остальной код эндпоинта /summary без изменений

@router.get("/summary")
def get_analytics_summary(
    currency: str = "BYN", 
    user_id: int = Depends(verify_tg_init_data), # Проверяем пользователя через Telegram initData
    db: Session = Depends(get_db)
):
    """
    Возвращает общую сумму доходов, расходов, текущий баланс 
    и разбивку расходов по категориям с учетом установленных лимитов.
    """
    
    # 1. Считаем общую сумму доходов пользователя в выбранной валюте
    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.telegram_user_id == user_id,
        Transaction.currency == currency,
        Transaction.type == "income"
    ).scalar() or 0.0

    # 2. Считаем общую сумму расходов пользователя в выбранной валюте
    total_expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.telegram_user_id == user_id,
        Transaction.currency == currency,
        Transaction.type == "expense"
    ).scalar() or 0.0

    # 3. Получаем сгруппированные расходы по категориям
    category_expenses = db.query(
        Transaction.category, 
        func.sum(Transaction.amount)
    ).filter(
        Transaction.telegram_user_id == user_id,
        Transaction.currency == currency,
        Transaction.type == "expense"
    ).group_by(Transaction.category).all()

    # 4. Подтягиваем лимиты бюджетирования пользователя для этой валюты
    limits = db.query(BudgetLimit).filter(
        BudgetLimit.telegram_user_id == user_id, 
        BudgetLimit.currency == currency
    ).all()
    limits_map = {l.category: l.limit_amount for l in limits}

    # 5. Формируем финальный массив категорий для фронтенда (для графиков и прогресс-баров)
    categories_data = []
    for cat, amt in category_expenses:
        categories_data.append({
            "category": cat,
            "amount": amt,
            "limit": limits_map.get(cat, 0.0) # Если лимит не установлен, вернет 0.0
        })

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "categories": categories_data
    }