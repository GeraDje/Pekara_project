from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers.router_auth import router_auth
from app.routers.router_prod_cart import router as router_cas
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники (не рекомендуется для продакшена)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(router_auth)
app.include_router(router_cas)