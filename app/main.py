from fastapi import FastAPI

from app.api.endpoints.charity_project import router as charity_router
from app.api.endpoints.donation import router as donation_router

app = FastAPI(title="QRKot")

app.include_router(charity_router, prefix="/charity_project", tags=["Проекты"])
app.include_router(donation_router, prefix="/donation", tags=["Пожертвования"])


@app.get("/")
async def root():
    """
    Корневой эндпоинт.

    Возвращает приветственное сообщение для проверки работоспособности API.
    """
    return {"message": "QRKot API"}
