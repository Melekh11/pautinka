"""
This module initializes and configures the FastAPI application.

The following functionalities are included:
- Loading environment variables using dotenv.
- Configuring logging for the application.
- Setting up CORS middleware to allow requests from specified origins.
- Including API routers for authentication, user management, and work reviews.
"""

import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.auth_routes import auth_router
from .routes.user_routes import user_router
from .routes.review_routes import review_router


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

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(review_router)
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
