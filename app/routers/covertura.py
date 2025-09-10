from fastapi import FastAPI, Depends, HTTPException, Request, Response, APIRouter
import os

from tools.sisa_conector import get_token, get_renaper, get_cobertura
import schemas.schemas as schemas

router = APIRouter(
    prefix="/covertura",
    tags=["covertura"]
)

@router.post("/", response_model=schemas.Coverturas)
async def covertura(dni: schemas.Persona):
    token = get_token()
    coverturas = get_cobertura(dni.nroDocumento, 1, token)

    if coverturas:
        return {
            "coverturas": coverturas
        }
