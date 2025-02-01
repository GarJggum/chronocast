# Chronocast SDK for Python

[![PyPI version](https://badge.fury.io/py/chronocast.svg)](https://pypi.org/project/chronocast/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Chronocast SDK empowers creators to build and stream AI-powered interactive experiences without coding expertise. From personalized AI hosts to dynamic storytelling, Chronocast's all-in-one toolkit integrates seamlessly with major streaming platforms and AI models, enabling content creators to focus on crafting engaging experiences while the SDK handles the technical complexity.

## Installation

```bash
pip install chronocast
```

For optional features, you can install extra dependencies:
```bash
# For audio features (text-to-speech, audio processing)
pip install "chronocast[audio_tools]"

# For visualization features
pip install "chronocast[matplotlib_tools]"

# For LangChain integration
pip install "chronocast[langchain_tools]"
```

## Quick Start

```python
from chronocast import Host, Experience, OpenaiModels, AudioTools

# Create an AI host for your experience
storyteller = Host(
    host_id="interactive_storyteller",
    role="Creative Storyteller",
    goal="Create engaging interactive stories",
    llm=OpenaiModels.gpt_4_turbo,
    tools={AudioTools.TextToSpeechTools}
)

# Create and start an interactive experience
experience = Experience.create(
    host=storyteller,
    title="The Adventure Begins",
    description="An interactive story where viewers' choices shape the narrative",
    stream_settings={
        "enable_voice": True,
        "enable_choices": True,
        "response_time": "dynamic"
    }
)
experience.start()
```

## Core Components

### Host
The Host class represents an AI personality that drives your interactive experiences. Hosts can be customized with:
- Unique personalities and roles
- Specific goals and objectives
- Custom tool sets
- Choice of AI models

```python
from chronocast import Host, AnthropicModels, AudioTools, WebTools

custom_host = Host(
    host_id="game_master",
    role="Interactive Game Master",
    goal="Create engaging RPG experiences",
    attributes="You are a creative and engaging game master who excels at creating immersive RPG experiences",
    llm=AnthropicModels.claude_3_opus,
    tools={AudioTools.TextToSpeechTools, WebTools.exa_search}
)
```

### Experience
The Experience class manages interactive content streams with real-time viewer engagement:
- Dynamic content generation
- Real-time viewer interaction
- Multi-modal content delivery
- Stream settings management

```python
from chronocast import Experience

experience = Experience.create(
    host=custom_host,
    title="Fantasy Adventure",
    description="An interactive RPG where viewers shape the story",
    stream_settings={
        "enable_voice": True,
        "enable_choices": True,
        "response_time": "dynamic",
        "interaction_mode": "multi_player"
    }
)
```

## Supported AI Models

Chronocast supports a wide range of AI models:

### OpenAI
- GPT-4 Turbo
- GPT-3.5 Turbo
- Custom models

### Anthropic
- Claude 3 Opus
- Claude 3 Sonnet
- Claude 3 Haiku

### Google
- Gemini Pro
- Gemini Ultra

### Mistral
- Mixtral
- Large

## Built-in Tools

### Content Creation
- Text-to-Speech conversion
- Audio processing and effects
- Image generation
- Dynamic visualization

### Interaction
- Real-time response processing
- Multi-choice management
- Sentiment analysis
- Dynamic adaptation

### Analytics
- Engagement tracking
- Performance metrics
- Content effectiveness
- Custom data collection

### Integration
- Streaming platforms
- External APIs
- Custom development

## Environment Setup

Chronocast uses environment variables for configuration. Create a `.env` file:

```env
# Required for OpenAI models
OPENAI_API_KEY=your_key_here

# Required for Anthropic models
ANTHROPIC_API_KEY=your_key_here

# Optional for additional features
ELEVENLABS_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
```

## Documentation

For detailed documentation, tutorials, and examples, visit:
- [Getting Started Guide](https://docs.chronocast.xyz/getting-started)
- [API Reference](https://docs.chronocast.xyz/api)
- [Examples & Tutorials](https://docs.chronocast.xyz/examples)
- [Best Practices](https://docs.chronocast.xyz/best-practices)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE.txt) file for details.

## Support

- [Documentation](https://docs.chronocast.xyz)
- [GitHub Issues](https://github.com/mainframecomputer/chronocast/issues)
- [Email Support](mailto:support@chronocast.xyz)
