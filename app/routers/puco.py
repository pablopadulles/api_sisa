from fastapi import FastAPI, Depends, HTTPException, Request, Response, APIRouter
import os

import schemas.schemas as schemas

router = APIRouter(
    prefix="/puco",
    tags=["puco"]
)

@router.post("/{dni}", response_model=schemas.LoginResponse)
async def login(dni, user: schemas.LoginRequest):
    # usuario = os.environ.get('USER_NO_FHIR')
    return{
        "samaccountname": dni,
        "ou": "string",
        "auth_token": "string"
        }
