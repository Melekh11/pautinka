import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.user import user_router
from database import create_db_and_tables

load_dotenv()
# print(os.environ)

origins = [
    "http://putinka.space",
    "https://pautinka.spase",
    "http://localhost",
    "http://localhost:8080",
]

print(os.getenv("DATABASE_URL"))
print(os.getenv)

app = FastAPI()

# create_db_and_tables()

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
