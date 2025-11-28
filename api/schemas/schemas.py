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
    cuil: str
    calle: str
    numero: str
    piso: Optional[str]
    departamento: Optional[str]
    cpostal: str
    barrio: str
    monoblock: Optional[str]
    ciudad: str
    municipio: str
    provincia: str
    pais: str
    mensaf: str
    origenf: str
    fechaf: str
    foto: Optional[str]
    sexo: str
    numeroDocumento: str
    fechaConsulta: str
    idciudadano: str
    descripcionError: str
    codigoError: int

class RenaperResponse(BaseModel):
    renaper: Renaper