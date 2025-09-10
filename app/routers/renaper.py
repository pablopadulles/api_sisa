from fastapi import FastAPI, Depends, HTTPException, Request, Response, APIRouter
import os

from tools.sisa_conector import get_token, get_renaper, get_cobertura
import schemas.schemas as schemas

router = APIRouter(
    prefix="/renaper",
    tags=["renaper"]
)

@router.post("/", response_model=schemas.RenaperResponse)
async def renaper(persona: schemas.Persona):
    token = get_token()
    renaper = get_renaper(persona.nroDocumento, persona.idSexo, token)

    if renaper:
        return {
            "renaper": renaper
        }
