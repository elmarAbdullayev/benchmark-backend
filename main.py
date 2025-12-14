# main.py
from fastapi import FastAPI
from servers.uvicorn import uvicorn_api
from servers.gunicorn import gunicorn_api
from db_queries import query_api  # falls du diese nutzt
from fastapi.middleware.cors import CORSMiddleware
from database import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# init DB
init_db()

app.include_router(uvicorn_api)
app.include_router(gunicorn_api)

@app.on_event("startup")
async def startup_event():
    print("API gestartet - Datenbank bereit!")

@app.get("/")
async def root():
    return {"message": "FastAPI Benchmark Server läuft"}
