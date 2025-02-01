# AI Models in Chronocast

Chronocast supports a wide range of AI models to power your interactive experiences. Each model has its own strengths, making them suitable for different types of content creation and viewer interaction.

## Supported Models

### OpenAI Models
Best for dynamic storytelling and real-time interaction:

```python
from chronocast import Host, OpenaiModels

storyteller = Host(
    host_id="storyteller",
    role="Creative Storyteller",
    llm=OpenaiModels.gpt_4_turbo  # Latest GPT-4 for dynamic content
)

game_host = Host(
    host_id="game_host",
    role="Game Show Host",
    llm=OpenaiModels.gpt_35_turbo  # Cost-effective for simpler interactions
)
```

### Anthropic Models
Excellent for educational content and complex narratives:

```python
from chronocast import Host, AnthropicModels

teacher = Host(
    host_id="science_teacher",
    role="Science Educator",
    llm=AnthropicModels.claude_3_opus  # Best for detailed explanations
)

story_writer = Host(
    host_id="novelist",
    role="Interactive Novelist",
    llm=AnthropicModels.claude_3_sonnet  # Balanced performance and cost
)
```

### Google Models
Great for multi-modal experiences:

```python
from chronocast import Host, GoogleModels

multimedia_host = Host(
    host_id="creative_host",
    role="Multimedia Creator",
    llm=GoogleModels.gemini_pro  # Strong multi-modal capabilities
)
```

### Mistral Models
Efficient for rapid interactions:

```python
from chronocast import Host, MistralModels

chat_host = Host(
    host_id="chat_moderator",
    role="Community Host",
    llm=MistralModels.mixtral  # Fast responses for chat moderation
)
```

## Model Selection Guide

### For Interactive Stories
- **Best Choice**: GPT-4 Turbo or Claude 3 Opus
- **Why**: Superior context understanding and narrative consistency
- **Cost-Effective Alternative**: GPT-3.5 Turbo or Claude 3 Sonnet

### For Educational Content
- **Best Choice**: Claude 3 Opus or GPT-4 Turbo
- **Why**: Excellent at detailed explanations and accurate information
- **Cost-Effective Alternative**: Claude 3 Sonnet

### For Game Shows
- **Best Choice**: GPT-3.5 Turbo or Mixtral
- **Why**: Fast responses and good performance/cost ratio
- **Cost-Effective Alternative**: Mistral Large

### For Multi-Modal Experiences
- **Best Choice**: Gemini Pro or GPT-4 Turbo Vision
- **Why**: Strong capabilities in handling multiple content types
- **Cost-Effective Alternative**: Gemini Pro Vision

## Model Configuration

### Temperature Settings
Control your Host's creativity level:

```python
# More creative, dynamic responses
creative_host = Host(
    host_id="creative_storyteller",
    llm=OpenaiModels.gpt_4_turbo,
    temperature=0.8  # Higher temperature for more variety
)

# More consistent, focused responses
factual_host = Host(
    host_id="educational_host",
    llm=AnthropicModels.claude_3_opus,
    temperature=0.3  # Lower temperature for consistency
)
```

### Response Length
Optimize for your content format:

```python
# Quick interactions
quick_host = Host(
    host_id="quiz_master",
    llm=MistralModels.mixtral,
    max_tokens=150  # Short, snappy responses
)

# Detailed content
detailed_host = Host(
    host_id="story_narrator",
    llm=AnthropicModels.claude_3_opus,
    max_tokens=1000  # Longer, more detailed responses
)
```

### Fallback Configuration
Ensure reliability with model fallbacks:

```python
from chronocast import Host, OpenaiModels, AnthropicModels

reliable_host = Host(
    host_id="reliable_host",
    role="Always-On Host",
    llm=[
        OpenaiModels.gpt_4_turbo,      # Primary model
        AnthropicModels.claude_3_opus,  # First fallback
        OpenaiModels.gpt_35_turbo      # Second fallback
    ]
)
```

## Best Practices

1. **Match Model to Content**: Choose models based on your content type and interaction needs
2. **Consider Costs**: Balance model capabilities with your budget
3. **Test Performance**: Evaluate models with your specific use case
4. **Configure Appropriately**: Adjust temperature and token limits for your needs
5. **Plan for Reliability**: Use fallback models for production environments

## Next Steps

- [Create Your First Host](agents.md)
- [Explore Available Tools](tools/index.md)
- [View Examples](https://docs.chronocast.xyz/examples)

