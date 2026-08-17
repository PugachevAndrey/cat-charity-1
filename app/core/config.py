from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения.

    Загружаются из переменных окружения или .env файла.
    Поля:
        app_title: Название приложения.
        database_url: URL для подключения к базе данных.
    """

    app_title: str = "QRKot"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"

    class Config:
        env_file = ".env"


settings = Settings()
