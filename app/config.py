from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    bot_token: str



    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env", env_file_encoding="utf-8",extra="ignore")

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

try:
    settings = Settings()
    print("Настройки успешно загружены:")
    print(f"DB_HOST: {settings.DB_HOST}")
    print(f"DB_PORT: {settings.DB_PORT}")
    print(f"DB_USER: {settings.DB_USER}")
    # Не выводим пароль и токен в лог для безопасности
except Exception as e:
    print(f"Ошибка загрузки настроек: {e}")
    print("Проверьте наличие файла .env в корне проекта")
    print("Пример содержимого .env:")
