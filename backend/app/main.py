from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import transactions, analytics # Импортируем оба роутера

# Автоматическое создание таблиц в SQLite при старте приложения
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Telegram Finance WebApp API")

# Настройка CORS для взаимодействия с будущим React-фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем модули нашего API
app.include_router(transactions.router)
app.include_router(analytics.router) # Новый роутер аналитики

@app.get("/")
def health_check():
    return {"status": "working", "database": "initialized"}