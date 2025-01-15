import os
import logging
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.user import user_router
from database import create_db_and_tables

load_dotenv(override=True)

logging.basicConfig(
    format="%(levelname)s:%(asctime)s:%(message)s", datefmt="%d/%m/%Y %I:%M:%S %p"
)
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

origins = [
    "http://putinka.space",
    "https://pautinka.spase",
    "http://localhost",
    "http://localhost:8080",
]


app = FastAPI()

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


@app.get("/ping")
async def pong():
    logger.info("pong")
    return "pong"
