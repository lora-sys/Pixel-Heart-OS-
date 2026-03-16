from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Get allowed origins from environment
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for app startup and shutdown."""
    # Startup
    print("Starting Pixel Heart OS Backend...")
    yield
    # Shutdown
    print("Shutting down Pixel Heart OS Backend...")


app = FastAPI(
    title="Pixel Heart OS Backend",
    description="AI-driven emergent social universe system backend",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Pixel Heart OS Backend"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/v1")
async def api_root():
    """API v1 root endpoint."""
    return {
        "version": "v1",
        "endpoints": [
            "/api/v1/health",
            "/api/v1/beads",
            "/api/v1/heroine",
            "/api/v1/npcs",
            "/api/v1/scenes",
            "/api/v1/simulation",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
