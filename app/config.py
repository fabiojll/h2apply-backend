import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    secret_key: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 dias

    # Last Link / Lemon Squeezy
    lemon_squeezy_api_key: str = Field(default="", env="LEMON_SQUEEZY_API_KEY")
    lemon_squeezy_store_id: str = Field(default="", env="LEMON_SQUEEZY_STORE_ID")
    lemon_squeezy_variant_id: str = Field(default="", env="LEMON_SQUEEZY_VARIANT_ID")
    lemon_squeezy_webhook_secret: str = Field(default="", env="LEMON_SQUEEZY_WEBHOOK_SECRET")

    frontend_url: str = Field(default="http://localhost:3000", env="FRONTEND_URL")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
