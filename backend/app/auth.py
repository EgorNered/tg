import hmac
import hashlib
import urllib.parse
import json
from fastapi import HTTPException, Header
from app.config import settings

async def verify_tg_init_data(authorization: str = Header(None)) -> int:
    """
    Декодирует заголовок Authorization, проверяет подпись Telegram.
    Если проверка успешна, возвращает чистый telegram_user_id.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Отсутствует заголовок Authorization")

    try:
        # Ожидаем формат заголовка: "Bearer строка_init_data"
        token_type, init_data = authorization.split(" ")
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Неверный тип токена")
            
        # Парсим строку параметров в словарь
        parsed_data = dict(urllib.parse.parse_qsl(init_data))
    except Exception:
        raise HTTPException(status_code=401, detail="Неверный формат авторизационных данных")

    if "hash" not in parsed_data:
        raise HTTPException(status_code=401, detail="Хэш Telegram не найден")

    # Вытаскиваем хэш, переданный Telegram, для последующего сравнения
    tg_hash = parsed_data.pop("hash")
    
    # Сортируем оставшиеся параметры по алфавиту и соединяем через перенос строки
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(parsed_data.items())])

    # Вычисляем секретный ключ на основе токена нашего бота
    secret_key = hmac.new(b"WebAppData", settings.BOT_TOKEN.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # Если хэши не совпадают, значит данные были изменены злоумышленником
    if calculated_hash != tg_hash:
        raise HTTPException(status_code=401, detail="Проверка целостности данных Telegram не пройдена")

    # Извлекаем JSON-объект пользователя
    try:
        user_data = json.loads(parsed_data.get("user", "{}"))
        user_id = user_data.get("id")
    except Exception:
        raise HTTPException(status_code=401, detail="Не удалось распарсить данные пользователя")
        
    if not user_id:
        raise HTTPException(status_code=401, detail="ID пользователя Telegram отсутствует")
        
    return user_id