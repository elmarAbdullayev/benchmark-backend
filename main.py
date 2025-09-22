from fastapi import FastAPI
from servers.uvicorn import uvicorn_api
from servers.gunicorn import gunicorn_api
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(uvicorn_api)
app.include_router(gunicorn_api)
