from pydantic import BaseModel
from typing import Optional, List

class cobertura(BaseModel):
    rnos: str
    cobertura: str
    servicio: str
    fechaConsulta: Optional[str] = None

class coberturas(BaseModel):
    coberturas: List[cobertura]

class Persona(BaseModel):
    nroDocumento: str
    idSexo: Optional[int] = None

class Renaper(BaseModel):
    idtramiteprincipal: int
    idtramitetarjetareimpresa: int
    ejemplar: str
    vencimiento: str
    emision: Optional[str]
    apellido: str
    nombres: str
    fechaNacimiento: str
    cuil: Optional[None]
    calle: Optional[None]
    numero: Optional[None]
    piso: Optional[str]
    departamento: Optional[str]
    cpostal: Optional[None]
    barrio: Optional[None]
    monoblock: Optional[str]
    ciudad: Optional[None]
    municipio: Optional[None]
    provincia: Optional[None]
    pais: Optional[None]
    mensaf: str
    origenf: str
    fechaf: str
    foto: Optional[str]
    sexo: str
    numeroDocumento: str
    fechaConsulta: str
    idciudadano: str
    descripcionError: Optional[None]
    codigoError: Optional[None]

class RenaperResponse(BaseModel):
    renaper: Renaper