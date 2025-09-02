
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from tools import redis_conection

# Middleware de autenticación con HTTPBearer (usaremos tokens Bearer)
auth_scheme = HTTPBearer()

# Dependency para verificar el token
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    res = await redis_conection.verify_token(token)
    if not res:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")
    return res

# Dependency para verificar el token
async def validate_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    if token != 'HNAP-123q':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")
    return True

