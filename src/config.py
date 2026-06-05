"""
Configuration management for the AI Application Compiler.
Handles environment variables, settings, and defaults.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class Config:
    """Central configuration for the application"""

    # Environment detection
    ENV = os.getenv("ENVIRONMENT", "development")
    DEBUG = ENV == "development"

    # Server configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))

    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter")
    LLM_MODEL = os.getenv("LLM_MODEL", "deepseek/deepseek-chat-v3-0324")
    LLM_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "4096"))

    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Compiler settings
    COMPILER_TIMEOUT = int(os.getenv("COMPILER_TIMEOUT", "60"))
    COMPILER_MAX_RETRIES = int(os.getenv("COMPILER_MAX_RETRIES", "3"))

    # Frontend configuration
    FRONTEND_BUILD_DIR = os.getenv("FRONTEND_BUILD_DIR", "build")
    STATIC_DIR = os.getenv("STATIC_DIR", "static")
    TEMPLATE_DIR = os.getenv("TEMPLATE_DIR", "templates")

    # Database (for future use)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///compiler.db")

    # CORS configuration
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

    # Feature flags
    ENABLE_CACHING = os.getenv("ENABLE_CACHING", "True") == "True"
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "True") == "True"

    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """
        Validate configuration on startup.
        Returns (is_valid, list_of_errors)
        """
        errors = []

        # Check required environment variables
        if not cls.LLM_API_KEY:
            errors.append(
                "OPENROUTER_API_KEY environment variable is required"
            )

        # Validate numeric ranges
        if cls.PORT < 1 or cls.PORT > 65535:
            errors.append(f"Invalid PORT: {cls.PORT}")

        if cls.LLM_TEMPERATURE < 0 or cls.LLM_TEMPERATURE > 2:
            errors.append(f"Invalid LLM_TEMPERATURE: {cls.LLM_TEMPERATURE}")

        if cls.COMPILER_TIMEOUT < 5:
            errors.append(f"COMPILER_TIMEOUT must be >= 5 seconds")

        # Validate LLM provider
        valid_providers = ["openrouter"]
        if cls.LLM_PROVIDER not in valid_providers:
            errors.append(
                f"Invalid LLM_PROVIDER. Must be one of: {', '.join(valid_providers)}"
            )

        return len(errors) == 0, errors

    @classmethod
    def setup_logging(cls) -> None:
        """Configure logging for the application"""
        logging.basicConfig(
            level=cls.LOG_LEVEL,
            format=cls.LOG_FORMAT,
        )
        logger.info(f"[Config] Initialized with environment: {cls.ENV}")
        logger.info(f"[Config] LLM Provider: {cls.LLM_PROVIDER}")
        logger.info(f"[Config] Log Level: {cls.LOG_LEVEL}")

    @classmethod
    def to_dict(cls) -> dict:
        """Convert configuration to dictionary (excluding secrets)"""
        return {
            "environment": cls.ENV,
            "debug": cls.DEBUG,
            "host": cls.HOST,
            "port": cls.PORT,
            "llm_provider": cls.LLM_PROVIDER,
            "llm_model": cls.LLM_MODEL,
            "log_level": cls.LOG_LEVEL,
            "compiler_timeout": cls.COMPILER_TIMEOUT,
            "compiler_max_retries": cls.COMPILER_MAX_RETRIES,
        }


# Development configuration
class DevelopmentConfig(Config):
    """Configuration for development environment"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"


# Production configuration
class ProductionConfig(Config):
    """Configuration for production environment"""
    DEBUG = False
    LOG_LEVEL = "INFO"
    ENABLE_CACHING = True


# Test configuration
class TestConfig(Config):
    """Configuration for testing"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    LLM_API_KEY = "test-key"


def get_config() -> Config:
    """Get appropriate config based on environment"""
    if Config.ENV == "production":
        return ProductionConfig()
    elif Config.ENV == "test":
        return TestConfig()
    else:
        return DevelopmentConfig()
