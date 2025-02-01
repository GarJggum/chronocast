# Welcome to Chronocast

Chronocast SDK empowers creators to build and stream AI-powered interactive experiences without coding expertise. From personalized AI hosts to dynamic storytelling, Chronocast's all-in-one toolkit integrates seamlessly with major streaming platforms and AI models, enabling content creators to focus on crafting engaging experiences while the SDK handles the technical complexity.

## Key Features

### No-Code Experience Creation
Build sophisticated AI-powered experiences without writing complex code. Our intuitive SDK handles the technical details, letting you focus on creativity.

### AI Host Integration
Create and customize AI hosts with unique personalities, goals, and capabilities. From storytellers to game masters, bring your interactive experiences to life.

### Real-Time Streaming
Seamlessly integrate with major streaming platforms. Manage live interactions, viewer engagement, and dynamic content delivery with built-in streaming support.

### Dynamic Content Generation
Create interactive narratives and responsive content on the fly. Let your AI hosts adapt and respond to viewer interactions in real-time.

### Multi-Modal Support
Handle text, audio, images, and more in your interactive experiences. Create rich, immersive content that engages your audience across multiple senses.

## Getting Started

### Installation
```bash
pip install chronocast
```

For optional features:
```bash
# Audio features
pip install "chronocast[audio_tools]"

# Visualization features
pip install "chronocast[matplotlib_tools]"
```

### Quick Example
```python
from chronocast import Host, Experience, OpenaiModels, AudioTools

# Create an AI host
storyteller = Host(
    host_id="interactive_storyteller",
    role="Creative Storyteller",
    goal="Create engaging interactive stories",
    llm=OpenaiModels.gpt_4_turbo,
    tools={AudioTools.TextToSpeechTools}
)

# Create and start an experience
experience = Experience.create(
    host=storyteller,
    title="The Adventure Begins",
    description="An interactive story where viewers shape the narrative",
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
The Host class represents an AI personality that drives your interactive experiences:
- Define unique personalities and roles
- Set specific goals and objectives
- Choose from various AI models
- Add custom tools and capabilities

### Experience
The Experience class manages your interactive content streams:
- Dynamic content generation
- Real-time viewer interaction
- Multi-modal content delivery
- Customizable stream settings

## Next Steps

- [Create Your First Host](agents.md)
- [Build an Interactive Experience](tasks.md)
- [Explore Available Tools](tools/index.md)
- [View Examples & Tutorials](https://docs.chronocast.xyz/examples)

## Support & Resources

- [API Reference](https://docs.chronocast.xyz/api)
- [Best Practices](https://docs.chronocast.xyz/best-practices)
- [GitHub Issues](https://github.com/mainframecomputer/chronocast/issues)
- [Email Support](mailto:support@chronocast.xyz)
