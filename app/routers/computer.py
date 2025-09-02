from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from tools import redis_conection
from tools.depends import get_current_user, validate_user
import schemas.schemas as schemas
from schemas.ActiveDirectoyConector import ActiveDirectoryConector
from typing import Optional
from operator import itemgetter

router = APIRouter(
    prefix="/ad_computer",
    tags=["ad_computer"]
)

# Endpoint para obtener el perfil del usuario autenticado
@router.get("/get_pcs")
async def get_pcs(name: Optional[str] = None):
    adc = ActiveDirectoryConector()
    if name:
        pcs = adc.get_pcs(name)
    else:
        pcs = adc.get_pcs()
    if not pcs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay pcs disponibles")

    pcs = sorted(pcs, key=itemgetter("CN"))

    return {
        "sise": len(pcs),
        "pc": pcs
    }

# # Endpoint para obtener el perfil del usuario autenticado
# @router.get("/del_pc")
# async def del_pc():
#     adc = ActiveDirectoryConector()
#     pcs = adc.delPV()
#     if not pcs:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay pcs disponibles")
#     return {
#         "pc": pcs,
#     }

@router.delete("/del_pc/{name}")
async def del_pc(name: str, user = Depends(validate_user)):
    adc = ActiveDirectoryConector()
    res = adc.delPV(name)

    if not res:
        raise HTTPException(status_code=404, detail="PC no encontrada")
    return {
        "msj": 'PC eliminada correctamente',
    }