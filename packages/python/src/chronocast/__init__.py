"""
Chronocast SDK: A Python framework for building and streaming AI-powered interactive experiences.
"""

__version__ = "0.0.24"

from .experience import StreamTask, configure_logging, LogColors, default_logger
from .host import Host
from .settings import Config
from .streaming import Stream, Experience, StreamInstruction
from .llm import (
    set_verbosity,
    OpenaiModels,
    OpenrouterModels,
    AnthropicModels,
    OllamaModels,
    GroqModels,
    TogetheraiModels,
    GeminiModels,
    DeepseekModels
)
from .tools import (
    FileTools,
    EmbeddingsTools,
    WebTools,
    GitHubTools,
    WikipediaTools,
    AmadeusTools,
    CalculatorTools,
    FAISSTools,
    PineconeTools,
    LinearTools,
    SemanticSplitter,
    SentenceSplitter,
    WhisperTools 
)

# Conditional imports for optional dependencies
import sys
import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tools.langchain_tools import LangchainTools
    from .tools.matplotlib_tools import MatplotlibTools
    from .tools.yahoo_finance_tools import YahooFinanceTools
    from .tools.fred_tools import FredTools
    from .tools.audio_tools import WhisperTools, TextToSpeechTools
    from .tools.stripe_tools import StripeTools 

def __getattr__(name):
    package_map = {
        "LangchainTools": (
            "langchain_tools",
            ["langchain-core", "langchain-community", "langchain-openai"],
        ),
        "MatplotlibTools": ("matplotlib_tools", ["matplotlib"]),
        "YahooFinanceTools": ("yahoo_finance_tools", ["yfinance", "yahoofinance"]),
        "FredTools": ("fred_tools", ["fredapi"]),
        "StripeTools": ("stripe_tools", ["stripe", "stripe_agent_toolkit"]),
        "TextToSpeechTools": ("audio_tools", ["elevenlabs", "pygame"]),
    }

    if name in package_map:
        module_name, required_packages = package_map[name]
        try:
            for package in required_packages:
                importlib.import_module(package)

            # If successful, import and return the tool
            module = __import__(f"chronocast.tools.{module_name}", fromlist=[name])
            return getattr(module, name)
        except ImportError as e:
            missing_packages = " ".join(required_packages)
            print(
                f"\033[95mError: The required packages ({missing_packages}) are not installed. "
                f"Please install them using 'pip install {missing_packages}'.\n"
                f"Specific error: {str(e)}\033[0m"
            )
            sys.exit(1)
    else:
        raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")


__all__ = [
    # Core Classes
    "StreamTask",
    "Host",
    "Stream",
    "Experience",
    "StreamInstruction",
    # Configuration and Utilities
    "Config",
    "settings",
    "helpers",
    "set_verbosity",
    # Logging
    "configure_logging",
    "LogColors",
    "default_logger",
    # LLM Provider Models
    "OpenaiModels",
    "AnthropicModels",
    "OpenrouterModels",
    "OllamaModels",
    "GroqModels",
    "TogetheraiModels",
    "GeminiModels",
    "DeepseekModels",
    # List core tools
    "FileTools",
    "EmbeddingsTools",
    "WebTools",
    "GitHubTools",
    "WikipediaTools",
    "AmadeusTools",
    "CalculatorTools",
    "FAISSTools",
    "PineconeTools",
    "LinearTools",
    "SemanticSplitter",
    "SentenceSplitter",
    "WhisperTools",
    # Optional tools
    "LangchainTools",
    "MatplotlibTools",
    "YahooFinanceTools",
    "TextToSpeechTools",
    "FredTools",
    "StripeTools",
]
