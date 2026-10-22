from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, cards
from app.models import Card, User

# Automatically create database tables on startup if they dont exist
Base.metadata.create_all(bind=engine)

# Instantiate the core FastAPI application object
app = FastAPI(
    title="Birthday Card API",
    version="1.0.0",
    description="API and enterprise backend for a birthday card scheduling and sending application, with user auth, JWT tokens and card vault storage.",
)

# Mount our modular routers into the application
app.include_router(auth.router)
app.include_router(cards.router)

@app.get("/")
def read_root():
    """Health check route verifying the API server is active."""
    return{
        "message": "Welcome to the Birthday Card API! Serving is running live.",
        "docs_url":"/docs",

    }