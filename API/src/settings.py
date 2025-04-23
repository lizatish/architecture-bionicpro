from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    FASTAPI_APP_KEYCLOAK_URL: str = "http://your-keycloak-server/auth/"
    FASTAPI_APP_KEYCLOAK_REALM: str = "your-realm"
    FASTAPI_APP_KEYCLOAK_CLIENT_ID: str = "your-client-id"
    FASTAPI_APP_KEYCLOAK_CLIENT_SECRET: str = "your-client-secret"  # Для confidential clients
    KEYCLOAK_DECODED_TOKEN_ALGORITHM: str = "RS256"

    GRANTED_USER_ROLE: str = "prothetic_user"

    FRONTEND_URL: str = "http://localhost:3000"


@lru_cache()
def get_settings():
    """Возвращает настройки тестов."""
    return Settings()
