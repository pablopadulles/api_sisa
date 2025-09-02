from fastapi import FastAPI
from routers import login, check, ad_attributes, computer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(login.router)
app.include_router(check.router)
app.include_router(ad_attributes.router)
app.include_router(computer.router)