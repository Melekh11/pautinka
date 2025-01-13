import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from helpers.crud import create_user
from routes.user import user_router
from database import create_db_and_tables

load_dotenv()

origins = [
    "http://putinka.space",
    "https://pautinka.spase",
    "http://localhost",
    "http://localhost:8080",
]

print(os.getenv("DATABASE_URL"))
print(os.getenv)

@asynccontextmanager
async def lifespan(app):
    print("tables created")
    
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
