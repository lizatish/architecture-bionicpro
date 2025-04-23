from keycloak import KeycloakOpenID

from settings import get_settings

conf = get_settings()

_instance: KeycloakOpenID | None = None


def init_keycloak_singleton() -> None:
    """Инициализация Keycloak клиента"""
    global _instance
    if _instance is None:
        _instance = KeycloakOpenID(
            server_url=conf.FASTAPI_APP_KEYCLOAK_URL,
            realm_name=conf.FASTAPI_APP_KEYCLOAK_REALM,
            client_id=conf.FASTAPI_APP_KEYCLOAK_CLIENT_ID,
            client_secret_key=conf.FASTAPI_APP_KEYCLOAK_CLIENT_SECRET,
        )
        # Предзагрузка сертификатов
        _instance.certs()


def get_keycloak_singleton() -> KeycloakOpenID:
    """Получение экземпляра Keycloak клиента"""
    if _instance is None:
        init_keycloak_singleton()
    return _instance


def close_keycloak_singleton() -> None:
    """Очистка ресурсов (если требуется)"""
    global _instance

    _instance = None
