from fastapi import FastAPI
from routers import covertura, renaper
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    """Configura logging con consola + archivo rotativo"""
    log_dir = "/var/log/sisa"
    os.makedirs(log_dir, exist_ok=True)

    logformat = '%(process)s %(thread)s [%(asctime)s] %(levelname)s %(name)s: %(message)s'
    logging.basicConfig(level=logging.INFO, format=logformat)

    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "app.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(logformat))
    root_logger = logging.getLogger()

    # Evita duplicar handlers en reload
    if not any(isinstance(h, RotatingFileHandler) for h in root_logger.handlers):
        root_logger.addHandler(file_handler)

    logging.getLogger(__name__).info("✅ Logging inicializado con lifespan")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 👉 Esto reemplaza a @app.on_event("startup")
    setup_logging()
    logging.getLogger(__name__).info("🚀 App iniciando con lifespan...")
    yield
    # 👉 Esto reemplaza a @app.on_event("shutdown")
    logging.getLogger(__name__).info("🛑 App finalizando...")
app = FastAPI()

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