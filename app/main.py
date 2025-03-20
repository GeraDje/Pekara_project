from fastapi import FastAPI
from app.auth.router import router_auth
app = FastAPI()

app.include_router(router_auth)