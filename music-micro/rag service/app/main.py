import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import admin, user
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="RAG Service (LangChain + Qdrant)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(user.router, tags=["user"])


@app.get("/health")
async def health():
    return {"status": "ok"}
