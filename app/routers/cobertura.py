from fastapi import FastAPI, Depends, HTTPException, Request, Response, APIRouter
import os
import logging

from tools.sisa_conector import get_token, get_renaper, get_cobertura
import schemas.schemas as schemas
import time

router = APIRouter(
    prefix="/cobertura",
    tags=["cobertura"]
)

@router.post("/", response_model=schemas.coberturas)
async def cobertura(dni: schemas.Persona):
    token = None 
    coberturas = None

    for _ in range(3):  # Intentar hasta 3 veces
        token = get_token()
        if token:
            break
        
    if not token:
        logging.error("No se pudo obtener el token después de varios intentos")
        raise HTTPException(status_code=500, detail="Error al obtener el token")

    for _ in range(3):  # Intentar hasta 3 veces
        coberturas = get_cobertura(dni.nroDocumento, 1, token)
        if coberturas:
            break
    
    
    if coberturas:
        return {
            "coberturas": coberturas
        }
    else:
        logging.error(f"Error al obtener coberturas para DNI {dni.nroDocumento}")
        raise HTTPException(status_code=404, detail="Error al obtener las coberturas")
