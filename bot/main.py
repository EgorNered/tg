import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Настраиваем логирование, чтобы видеть ошибки в терминале
logging.basicConfig(level=logging.INFO)

# Читаем токен бота и URL из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://localhost:3000")

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    """Обработчик команды /start"""
    # Создаем инлайн-кнопку, которая развернет наш WebApp
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть Кошелёк 💰", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n\n"
        "Добро пожаловать в BNB Finance — приложение для учёта личных финансов.\n\n"
        "👉 Нажми на кнопку ниже, чтобы открыть графики, внести доходы/расходы и настроить лимиты бюджета бюджета прямо внутри Telegram!",
        reply_markup=kb
    )

async def main():
    print("Бот BNB Finance успешно запущен в режиме Long Polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())