# Copyright 2024 Mainframe-Orchestra Contributors. Licensed under Apache License 2.0.

from zoneinfo import ZoneInfo
from abc import ABC, abstractmethod
import os
from typing import Optional


class Config(ABC):
    """
    Base configuration class for Chronocast SDK settings.
    
    This class manages essential settings for interactive streaming experiences,
    including AI model credentials, timezone preferences, and other configuration
    parameters that affect content creation and delivery.
    """

    DEFAULT_TIMEZONE = ZoneInfo("America/New_York")

    # AI Model Provider API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    TOGETHERAI_API_KEY: Optional[str] = None

    @classmethod
    def validate_api_key(cls, key_name: str) -> str:
        """
        Validate and return a specific AI provider's API key.
        
        This method ensures that the necessary credentials are available
        for accessing AI models used in content creation.
        """
        key_value = getattr(cls, key_name, None) or os.getenv(key_name)
        if not key_value:
            raise ValueError(f"{key_name} environment variable is not set")
        return key_value

    @classmethod
    @abstractmethod
    def validate_required_env_vars(cls) -> None:
        """
        Validate all required environment variables for the streaming experience.
        
        Subclasses should implement this method to ensure all necessary
        configuration parameters are properly set.
        """
        raise NotImplementedError("Subclasses must implement validate_required_env_vars")


class EnvConfig(Config):
    """
    Environment-based configuration for Chronocast SDK.
    
    This class provides a simple way to configure the SDK using environment
    variables, making it easy to set up and deploy interactive streaming
    experiences in different environments.
    """

    def __init__(self):
        # Initialize AI Model Provider API Keys from environment variables
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.TOGETHERAI_API_KEY = os.getenv("TOGETHERAI_API_KEY")

    @classmethod
    def validate_required_env_vars(cls) -> None:
        """
        Validate that all required environment variables are set.
        
        This implementation allows for flexible configuration where any
        combination of AI providers can be used based on available credentials.
        """
        pass  # No specific requirements - keys are validated on use


config = EnvConfig()