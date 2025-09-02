from secrets import token_hex

from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from tools import redis_conection
from tools.depends import get_current_user
import schemas.schemas as schemas
from schemas.ActiveDirectoyConector import ActiveDirectoryConector

router = APIRouter(
    prefix="/check",
    tags=["check"]
)


@router.get("/validatetoken", response_model=schemas.CheckResponse)
async def check(current_user: str = Depends(get_current_user)):
    if current_user:
        return {"valid": True, "samaccountname": current_user}
    raise HTTPException(status_code=400, detail="Session expired")

@router.get("/validate_email_token")
async def validate_email_token(token: str):
    samaccountname = await redis_conection.verify_email_token(token)
    if samaccountname:
        return {"samaccountname": samaccountname}
    else:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

# @router.post("/validate_token", response_model=schemas.CheckResponse)
# async def check(token: schemas.CheckRequest):
#     res = await redis_conection.verify_token(token.token)
#     if not res:
#         raise HTTPException(status_code=400, detail="Session expired")
#     print(res)
#     return {"valid": True, "samaccountname": res}

