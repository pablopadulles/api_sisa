from fastapi import FastAPI
from routers import covertura, renaper
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from tools.setup_logging import setup_logging
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 👉 Esto reemplaza a @app.on_event("startup")
    setup_logging()
    logging.getLogger(__name__).info("App iniciando con lifespan...")
    yield
    # 👉 Esto reemplaza a @app.on_event("shutdown")
    logging.getLogger(__name__).info("App finalizando...")

app = FastAPI(lifespan=lifespan)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(covertura.router)
app.include_router(renaper.router)
# app.include_router(check.router)
# app.include_router(ad_attributes.router)
# app.include_router(computer.router)