from typing import Optional
from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = "Кошачий благотворительный фонд"
    app_desc: str = None
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    secret: str = 'secret'

    class Config:
        env_file = ".env"


settings = Settings()
