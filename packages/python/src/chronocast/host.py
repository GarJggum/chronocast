from pydantic import BaseModel, Field
from typing import Optional, Callable, Union, Set, List


class Host(BaseModel):
    """
    Represents an AI host that creates and manages interactive streaming experiences.
    
    A host is responsible for engaging with users through dynamic content generation,
    storytelling, and real-time interaction using various AI models and tools.
    """
    
    host_id: str = Field(..., description="The unique identifier for the AI host")
    role: str = Field(..., description="The persona or character type of the AI host")
    goal: str = Field(..., description="The objective or purpose of the interactive experience")
    attributes: Optional[str] = Field(
        None, description="Additional personality traits or characteristics of the AI host"
    )
    llm: Optional[Union[Callable, List[Callable]]] = Field(
        None,
        description="The AI model function(s) powering the host's interactions. Can be a single model or a list for fallback",
    )
    tools: Optional[Set[Callable]] = Field(
        default=None,
        description="Optional set of tools for enhancing the interactive experience (e.g., media handling, data processing)",
    )
    temperature: Optional[float] = Field(
        default=0.7, description="Creativity level for the AI model's responses. Higher values (0-1) increase creativity"
    )
    max_tokens: Optional[int] = Field(
        default=4000,
        description="Maximum length of the AI model's responses in tokens. Default is 4000",
    )
    model_config = {"arbitrary_types_allowed": True}
