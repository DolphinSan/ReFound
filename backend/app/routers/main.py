from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import auth, items, dashboard
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ReFound API",
    description="Lost & Found Campus System - Institut Teknologi Sepuluh Nopember",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# foto upload
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(items.router)
app.include_router(dashboard.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "app": "ReFound API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }
