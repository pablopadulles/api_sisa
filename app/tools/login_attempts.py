from fastapi import Request, HTTPException, status
import redis.asyncio as redis
import os
from contextlib import asynccontextmanager

if os.getenv('REDIS_URL', False):
    REDIS_URL = os.getenv('REDIS_URL')
else:
    REDIS_URL = 'redis://redis:6379'

EXPIRE = os.getenv('EXPIRE', 600)
MAX_ATTEMPTS = os.getenv('MAX_ATTEMPTS', 5)  # Número máximo de intentos permitidos
LOCK_TIME = os.getenv('MAX_ATTEMPTS', 600)  # Tiempo de bloqueo en segundos (10 minutos)

redis_cli = None

@asynccontextmanager
async def close_redis():
    global redis_cli
    if redis_cli:
        redis_cli.close()
        await redis_cli.wait_closed()

@asynccontextmanager
async def get_redis():
    global redis_cli
    if not redis_cli:
        redis_cli = await redis.from_url(REDIS_URL)
    try:
        yield redis_cli
    finally:
        pass

async def check_login_attempts(request: Request, user:str):
    client_ip = get_ip(request)
    login_attempts = await get_login_attempts(user, client_ip)
    validate_login_attempts(login_attempts)
    return True

def get_ip(request: Request):
    # Primero intenta obtener la IP desde el encabezado "X-Forwarded-For"
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        client_ip = forwarded.split(",")[0]
    else:
        client_ip = request.client.host  
    return client_ip

async def get_login_attempts(username: str, client_ip: str):
    res = {}
    async with get_redis() as redis:
        attempts = await redis.get(f"login_attempts:{username}")
        res['user'] = 0 if attempts is None else int(attempts)
        attempts = await redis.get(f"login_attempts:{client_ip}")
        res['client_ip'] = 0 if attempts is None else int(attempts)
    return res

def validate_login_attempts(login_attempts: dict):
    for key in login_attempts.keys():
        if login_attempts[key] >= MAX_ATTEMPTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many login attempts. Please try again later."
            )

async def increment_login_attempts(request: Request, user:str):
    client_ip = get_ip(request)
    async with get_redis() as redis:
        attempts = get_login_attempts(user, client_ip)
        for key in attempts.keys():
            attempts[key] += 1
            await redis.setex(f"login_attempts:{key}", LOCK_TIME, attempts)

async def reset_login_attempts(request: Request, user:str):
    client_ip = get_ip(request)
    async with get_redis() as redis:
        await redis.delete(f"login_attempts:{client_ip}")
        await redis.delete(f"login_attempts:{user}")
