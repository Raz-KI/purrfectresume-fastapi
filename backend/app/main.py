from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Perfect Resume API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://purrfectresume-fastapi.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
