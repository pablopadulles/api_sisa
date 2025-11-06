from fastapi import FastAPI, Depends, HTTPException, Request, Response, APIRouter
import os
import logging

from tools.sisa_conector import get_token, get_renaper
import schemas.schemas as schemas

router = APIRouter(
    prefix="/renaper",
    tags=["renaper"]
)

@router.post("/", response_model=schemas.RenaperResponse)
async def renaper(persona: schemas.Persona):

    for _ in range(3):  # Intentar hasta 3 veces
        token = get_token()
        if token:
            break

    if not token:
        logging.error("No se pudo obtener el token después de varios intentos")
        raise HTTPException(status_code=500, detail="Error al obtener el token")

    for _ in range(3):  # Intentar hasta 3 veces
        renaper = get_renaper(persona.nroDocumento, persona.idSexo, token)
        if renaper:
            break

    if renaper:
        return {
            "renaper": renaper
        }
    else:
        logging.error(f"Error al obtener Renaper para DNI {persona.nroDocumento}")
        raise HTTPException(status_code=404, detail="Error al obtener los datos de Renaper")
