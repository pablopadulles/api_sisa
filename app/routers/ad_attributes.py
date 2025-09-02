from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from tools import redis_conection
from tools.depends import get_current_user, validate_user
import schemas.schemas as schemas
from schemas.ActiveDirectoyConector import ActiveDirectoryConector

router = APIRouter(
    prefix="/ad_attributes",
    tags=["ad_attributes"]
)

# Endpoint para obtener el perfil del usuario autenticado
@router.get("/profile")
async def get_profile(current_user: str = Depends(get_current_user)):
    adc = ActiveDirectoryConector()
    user_data = adc.search_user(str(current_user))
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return {
        "mail": user_data["mail"],
        "cn": user_data["cn"],
        "telephoneNumber": user_data["telephoneNumber"]
    }

# Endpoint para buscar
@router.get("/profile/{user}")
async def get_user(user, current_user: str = Depends(validate_user)):
    adc = ActiveDirectoryConector()
    user_data = adc.search_user(str(user))
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return {
        "mail": user_data["mail"],
        "cn": user_data["cn"],
        "telephoneNumber": user_data["telephoneNumber"]
    }

# # Endpoint para actualizar el perfil del usuario autenticado
@router.put("/profile")
async def update_profile(profile: schemas.ProfileUpdate, current_user: str = Depends(get_current_user)):
    adc = ActiveDirectoryConector()
    dominio = profile.mail.split('@')[1]
    if dominio in ['hospitalposadas.gob.ar', 'hospitalposadas.gov.ar']:
        atts = {
            "mail": profile.mail,
            # "cn": profile.cn,
            "telephoneNumber": profile.telephoneNumber
        }
        if adc.set_attributes(current_user, atts):
            return {"message": "Perfil actualizado correctamente"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

@router.get("/get_users_group/{group}")
async def get_users_group(group: str):
    adc = ActiveDirectoryConector()
    users = adc.get_users_group(group)
    if users:
        return {"users": users}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron usuarios en el grupo especificado")