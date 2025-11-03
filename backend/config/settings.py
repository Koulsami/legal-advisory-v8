"""
Settings and configuration for Legal Advisory System v8.0
Uses pydantic-settings for environment variable management
"""

from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """

    # Application
    APP_NAME: str = "Legal Advisory System v8.0"
    APP_VERSION: str = "8.0.0-alpha"
    DEBUG: bool = False

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v8"

    # Elasticsearch - Three-Stage Retrieval
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_INDEX: str = "singapore_legal_v8"

    # PostgreSQL
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "legal_advisory_v8"
    POSTGRES_USER: str = "legal_user"
    POSTGRES_PASSWORD: str = "legal_password_change_in_prod"

    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Neo4j - Knowledge Graph
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "legal_password_change_in_prod"

    # Redis - Caching
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @property
    def REDIS_URL(self) -> str:
        """Construct Redis URL"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # AI Models
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

    # Legal-BERT for semantic search
    LEGAL_BERT_MODEL: str = "nlpaueb/legal-bert-base-uncased"
    EMBEDDINGS_CACHE_DIR: str = "backend/retrieval/embeddings/cache"

    # FAISS Index
    FAISS_INDEX_PATH: str = "backend/retrieval/indexes/order21.faiss"
    FAISS_DIMENSION: int = 768  # Legal-BERT embedding dimension

    # Citation Database
    CITATION_DB_PATH: str = "backend/verification/data/citations.db"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Security
    SECRET_KEY: str = "change_this_in_production_to_random_string"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # MCP Servers
    MCP_REGISTRY_URL: str = "http://localhost:8001"
    MCP_RETRIEVAL_URL: str = "http://localhost:8002"
    MCP_VERIFICATION_URL: str = "http://localhost:8003"
    MCP_CALCULATION_URL: str = "http://localhost:8004"

    # Performance
    MAX_WORKERS: int = 4
    CACHE_TTL: int = 3600  # 1 hour

    # Retrieval Settings (from research)
    BM25_K1: float = 1.5  # Tuned for legal documents
    BM25_B: float = 0.75
    RETRIEVAL_STAGE1_WEIGHT: float = 0.3  # BM25
    RETRIEVAL_STAGE2_WEIGHT: float = 0.3  # Semantic
    RETRIEVAL_STAGE3_WEIGHT: float = 0.4  # Legal classification

    # Verification Settings
    HALLUCINATION_THRESHOLD: float = 0.1  # 10%
    TEXT_ALIGNMENT_THRESHOLD: float = 0.7  # 70%

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Only loads once per application lifecycle
    """
    return Settings()
