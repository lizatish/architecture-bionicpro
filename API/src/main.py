import logging
from contextlib import asynccontextmanager

import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes import router
from auth.keycloak_singleton import init_keycloak_singleton, close_keycloak_singleton
from settings import get_settings

conf = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_keycloak_singleton()
    yield
    close_keycloak_singleton()


app = FastAPI(
    title="Reports API",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[conf.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, tags=['reports'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level=logging.DEBUG,
    )
