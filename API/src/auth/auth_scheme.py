from fastapi.security import OAuth2AuthorizationCodeBearer

from settings import get_settings

conf = get_settings()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{conf.FASTAPI_APP_KEYCLOAK_URL}realms/{conf.FASTAPI_APP_KEYCLOAK_REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{conf.FASTAPI_APP_KEYCLOAK_URL}realms/{conf.FASTAPI_APP_KEYCLOAK_REALM}/protocol/openid-connect/token",
)
