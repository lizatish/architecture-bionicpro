import time

from fastapi import Depends, HTTPException
from jose import JWTError
from starlette import status

from auth.auth_scheme import oauth2_scheme
from auth.keycloak_singleton import get_keycloak_singleton
from settings import get_settings

conf = get_settings()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Декодирование и проверка токена
        keycloak_openid = get_keycloak_singleton()
        decoded_token = keycloak_openid.decode_token(token)

        # Проверка срока действия токена
        if decoded_token["exp"] < time.time():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )

        return decoded_token
    except JWTError as e:
        raise conf.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


async def check_granted_user_role(user: dict = Depends(get_current_user)):
    if conf.GRANTED_USER_ROLE not in user.get("realm_access", {}).get("roles", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return user
