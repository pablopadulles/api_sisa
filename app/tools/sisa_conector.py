import requests
import os
from fastapi import HTTPException

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"  # algunos servidores lo requieren
}

data = {
    "nombre": os.environ.get("USER_NO_FHIR", False),
    "clave": os.environ.get("PASS_NO_FHIR", False),
    "codDominio": os.environ.get("CODE_DOMAIN", False),
}

def get_token():
    r = requests.post(
        "https://bus.msal.gob.ar/masterfile-federacion-service/api/usuarios/aplicacion/login",
        json=data,
        headers=headers,
        verify=False,
        timeout=5
    )
    res = r.json()
    token = res.get('token')
    return token

def get_renaper(dni, sexo, token):
    headers.update({'token': token, 'codDominio': os.environ.get("CODE_DOMAIN", False)})
    url = f"https://bus.msal.gob.ar/masterfile-federacion-service/api/personas/renaper?nroDocumento={dni}&idSexo={sexo}"

    r = requests.get(
        url,
        headers=headers,
        verify=False,
        timeout=5
    )
    if r.status_code != 200:
        raise HTTPException(status_code=404, detail="Verificar el sexo o el DNI")
    
    res = r.json()
    return res

def get_cobertura(dni, sexo, token):
    headers.update({'token': token, 'codDominio': os.environ.get("CODE_DOMAIN", False)})
    url = f"https://bus.msal.gob.ar/masterfile-federacion-service/api/personas/cobertura?nroDocumento={dni}&idSexo={sexo}"
    r = requests.get(
        url,
        headers=headers,
        verify=False,
        timeout=5
    )

    res = r.json()
    return res

