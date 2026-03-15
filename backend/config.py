"""
Configuration management for Pixel Heart OS backend.
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM - Choose provider: "anthropic", "stepfun", or "mock"
    llm_provider: str = "anthropic"
    anthropic_api_key: str = ""
    stepfun_api_key: str = ""
    stepfun_base_url: str = "https://api.stepfun.com"
    llm_model: str = "claude-3-5-sonnet-20241022"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 4000

    # Database
    database_url: str = "sqlite+aiosqlite:///./pixel_heart.db"
    chroma_db_path: str = "./chroma_db"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    allowed_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Logging
    log_level: str = "INFO"

    # Data Storage - use absolute path
    data_dir: Path = Path(__file__).parent.parent / "data"

    # Mock mode (for testing without API key)
    use_mock_llm: bool = False

    # Caching
    cache_ttl_beads: int = 60  # seconds
    cache_ttl_heroine: int = 120
    cache_ttl_npcs: int = 120

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

# Initialize singleton services (lazy init on startup)
_bead_engine: Optional["BeadEngine"] = None
_llm_service: Optional["LLMService"] = None
_chroma_client: Optional["ChromaClient"] = None


def get_bead_engine() -> "BeadEngine":
    """Get or create BeadEngine singleton."""
    global _bead_engine
    if _bead_engine is None:
        from beads.engine import BeadEngine
        _bead_engine = BeadEngine()
    return _bead_engine


def get_llm_service() -> "LLMService":
    """Get or create LLMService singleton."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


def get_chroma_client() -> "ChromaClient":
    """Get or create ChromaClient singleton."""
    global _chroma_client
    if _chroma_client is None:
        from vector_store.chroma_client import ChromaClient
        _chroma_client = ChromaClient(persist_directory=settings.chroma_db_path)
    return _chroma_client
