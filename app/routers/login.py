from fastapi import FastAPI, Depends, HTTPException, Request, Response, APIRouter
from secrets import token_hex
from tools import redis_conection, login_attempts
from tools.send_email import send_email
import os

import schemas.schemas as schemas
from schemas.ActiveDirectoyConector import ActiveDirectoryConector

router = APIRouter(
    prefix="/login",
    tags=["login"]
)

@router.post("/", response_model=schemas.LoginResponse)
async def login(response: Response, user: schemas.LoginRequest, request: Request):
    usuario = os.environ.get('USER_NO_FHIR')
    await login_attempts.check_login_attempts(request, user.samaccountname)
    adc = ActiveDirectoryConector()
    if adc.authenticate(user.samaccountname, user.password):
        token = token_hex()
        await redis_conection.create_token(user.samaccountname, token)
        data = adc.search_user(user.samaccountname)
    else:
        await login_attempts.increment_login_attempts(request, user.samaccountname)
        raise HTTPException(status_code=400, detail="Error de usuario o contraseña")
    
    return {'samaccountname': data['sAMAccountName'], 'ou':data['distinguishedName'], 'auth_token':token}


@router.post("/forgot-password")
async def forgot_password(samaccountname: schemas.LoginForgotPasswordRequest):
    adc = ActiveDirectoryConector()
    attrs = adc.search_user(samaccountname.samaccountname)

    if attrs['mail']:
        await send_email(attrs['mail'], {
            'samaccountname':samaccountname.samaccountname,
            'distinguishedName': attrs['cn']})
        return {'mail': attrs['mail']}
    
    HTTPException(status_code=400, detail="Error en el receteo de password")
    
@router.post("/reset-password")
async def reset_password(request: schemas.ResetPasswordRequest):
    samaccountname = await redis_conection.verify_email_token(request.token)
    adc = ActiveDirectoryConector()
    if not adc.set_pass(samaccountname, request.new_password) or not samaccountname:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    return {"message": "Contraseña actualizada correctamente"}