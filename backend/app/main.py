from fastapi import FastAPI
from app.api.routes import router # Comment this when pushing to git
# from api.routes import router # Comment this when running on local

app = FastAPI(title="Perfect Resume API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
