from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LoginForgotPasswordRequest(BaseModel):
    samaccountname: str
    
class LoginRequest(BaseModel):
    samaccountname: str
    password: str

class LoginResponse(BaseModel):
    samaccountname: str
    ou: str
    auth_token: str
    
class CheckRequest(BaseModel):
    token: str

class CheckResponse(BaseModel):
    valid: bool
    samaccountname: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    
class ProfileUpdate(BaseModel):
    mail: Optional[str] = None
    telephoneNumber: Optional[str] = None
    cn: Optional[str] = None

class AppsResponse(BaseModel):
    apps: list
