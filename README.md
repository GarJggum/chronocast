# Chronocast

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/mainframecomputer/chronocast/issues)
[![PyPI version](https://badge.fury.io/py/chronocast.svg)](https://pypi.org/project/chronocast/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Chronocast SDK empowers creators to build and stream AI-powered interactive experiences without coding expertise. From personalized AI hosts to dynamic storytelling, Chronocast's all-in-one toolkit integrates seamlessly with major streaming platforms and AI models, enabling content creators to focus on crafting engaging experiences while the SDK handles the technical complexity.

## 🌟 Features

- **No-Code Experience Creation**: Build sophisticated AI-powered experiences without writing complex code
- **AI Host Integration**: Create and customize AI hosts with unique personalities and capabilities
- **Real-Time Streaming**: Seamless integration with major streaming platforms
- **Dynamic Content Generation**: Create interactive narratives and responsive content on the fly
- **Multi-Modal Support**: Handle text, audio, images, and more in your interactive experiences

## 📦 Packages

### Python SDK
The core Chronocast SDK for Python, enabling rapid development of interactive experiences.
```bash
pip install chronocast
```
[Learn more about the Python SDK](packages/python/README.md)

## 🚀 Quick Example

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

## 📚 Documentation

- [Getting Started Guide](https://docs.chronocast.xyz/getting-started)
- [API Reference](https://docs.chronocast.xyz/api)
- [Examples & Tutorials](https://docs.chronocast.xyz/examples)
- [Best Practices](https://docs.chronocast.xyz/best-practices)

## 🤝 Contributing

We welcome contributions! Whether it's bug reports, feature requests, or code contributions, check out our [Contributing Guidelines](CONTRIBUTING.md).

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE.txt) file for details.

## 💬 Community & Support

- [Documentation](https://docs.chronocast.xyz)
- [GitHub Issues](https://github.com/mainframecomputer/chronocast/issues)
- [Email Support](mailto:support@chronocast.xyz)
