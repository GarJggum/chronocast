# Agents

Agents in Orchestra are components that encapsulate specific personas to be assigned to tasks. They are designed to perform tasks in a manner consistent with their defined role, goal, and attributes. Agents are typically configured with a specific LLM and, if needed, a set of tools tailored to their role, enabling them to effectively execute their assigned tasks.

The reusability of agents in Orchestra not only streamlines workflow design but also contributes to the overall consistency of output. By utilizing the same agent across different tasks within its area of expertise, you can expect uniform behavior and response styles, which is particularly valuable in maintaining a coherent user experience or adhering to specific operational standards.

### Configuring Agent Intelligence and Capabilities

In Orchestra, agents can be further customized by setting specific LLMs and tool sets. This configuration allows you to fine-tune the agent's intelligence level, associated costs, and functional capabilities, effectively creating specialized teams of agents.

### Anatomy of an Agent

An agent in Orchestra is defined by four core components:

- **role**: Defines the agent's purpose or function within the Orchestra workflow. e.g. "Web Researcher".
- **goal**: Specifies the desired outcome or objective that the agent aims to achieve. e.g. "find relevant Python agent repositories with open issues".
- **attributes** (Optional): Additional characteristics or traits that shape the agent's behavior and personality. e.g. "analytical, detail-oriented, and determined to write thorough reports".
- **llm**: The underlying language model assigned to the agent for generating responses. e.g. `OpenrouterModels.haiku`.

### Creating an Agent

To create an agent in Orchestra, you can use the Agent class provided by the library. Here's an example:

```python
from mainframe_orchestra import Agent, OpenrouterModels

customer_support_agent = Agent(
    role="customer support representative",
    goal="to resolve customer inquiries accurately and efficiently",
    attributes="friendly, empathetic, and knowledgeable about the product",
    llm=OpenrouterModels.haiku
)
```

### Assigning Agents to Tasks

Here's an example demonstrating how an agent can be created and then integrated into multiple tasks within a Orchestra workflow:

```python
from mainframe_orchestra import Task, Agent, OpenrouterModels

data_analyst_agent = Agent(
    role="data analyst",
    goal="to provide insights and recommendations based on data analysis",
    attributes="analytical, detail-oriented, and proficient in statistical methods",
    llm=OpenrouterModels.haiku
)

def analysis_task (sales_data):
    return Task.create(
       agent=data_analyst_agent,
       context=f"The sales data for the past quarter is attached: '{sales_data}'.",
       instruction="Analyze the sales data and provide recommendations for improving revenue."
    )
```

### Assigning Tools to Agents

Agents can be assigned tools to enhance their capabilities and enable them to perform specific actions. Tools are functions that the agent can use to interact with external systems, process data, or perform specialized tasks. 

The agent will have the opportunity to use tools provided to the agent or the task to assist in its completion. The tools are passed to the agent's 'tools' parameter during initialization, and the agent will then be able to see and use the tools before completing their final response. They can call tools once, recursively, or multiple times in parallel. For more on tool use see the [tool use](./tool-use) page.

Here's an example of assigning tools to an agent:

```python
from mainframe_orchestra import Agent, GitHubTools, OpenaiModels

researcher = Agent(
    role="GitHub researcher",
    goal="find relevant Python agent repositories with open issues",
    attributes="analytical, detail-oriented, able to assess repository relevance and popularity",
    llm=OpenaiModels.gpt_4o_mini,
    tools={GitHubTools.search_repositories, GitHubTools.get_repo_details}
)
```

In this example, the researcher agent is assigned two tools from the GitHubTools module. These tools allow the agent to search for repositories and get repository details, which are essential for its role as a GitHub researcher. Tools are passed to the agent's 'tools' parameter during initialization.

##### Advanced Agent Parameters

Agents can be assigned additional parameters to tune their behavior. These additional params control model temperature and max tokens. Default temperature is 0.7 and max tokens is 4000. You can set temperature and max tokens in the agent definition and they will override the defaults set in the llm. Here's an example:

```python
from mainframe_orchestra import Agent, OpenrouterModels

assistant_agent = Agent(
    role="assistant",
    goal="to provide insights and recommendations based on data analysis",
    llm=OpenrouterModels.haiku,
    max_tokens=500,
    temperature=0.5
)
```

These additional settings are optional and are often not required unless custom or specific temperature and max tokens are required. The default temperature of 0.7 and max tokens of 4000 covers most use cases, but programming or long responses may benefit from custom temperature and max tokens.

#### LLM Fallbacks via Lists

You can now specify multiple LLMs for a task, allowing for automatic fallback if the primary LLM fails or times out.

In this example, if `AnthropicModels.sonnet_3_5` fails (e.g., due to rate limiting), the task automatically falls back to `AnthropicModels.haiku_3_5`. You can specify as many LLMs as you want in the list and they will be tried in order. You can have the models fall back to another of the same provider, or you can have them fall back to a different provider if the provider itself fails. This is useful for handling rate limits or other failures that may occur with certain LLMs, particularly in a production environment.

```python
from mainframe_orchestra import Agent, GitHubTools, AnthropicModels

researcher = Agent(
    role="GitHub researcher",
    goal="find relevant Python agent repositories with open issues",
    attributes="analytical, detail-oriented, able to assess repository relevance and popularity",
    llm=[AnthropicModels.sonnet_3_5, AnthropicModels.haiku_3_5],
    tools={GitHubTools.search_repositories, GitHubTools.get_repo_details}
)
```

##### Prompting

Prompting involves crafting effective prompts for agent roles, goals, and attributes to elicit desired behaviors and responses from the language model. Here are some tips for effective prompting:

- Use clear and concise language that captures the essence of the agent's role and goal.
- Use the optional attributes field to provide additional behavioral cues and suggestions based on feedback from tests.
- Experiment with different prompt variations and evaluate their impact on agent performance.
- Use the attributes field to provide additional behavioral cues and suggestions based on feedback from tests".

Testing and iterative development is key to creating effective prompts. The feedback from the initial runs will be used to refine the prompts and improve the performance of the agents. It's worth testing and adjusting early in the process as you develop out your multi-agent team or workflows.

By incorporating these advanced techniques, you can create agents that can handle complex tasks, adapt to user preferences, and provide more personalized and context-aware responses.

# Creating AI Hosts

In Chronocast, Hosts are the AI personalities that drive your interactive experiences. Each Host can be customized with unique traits, capabilities, and goals to create engaging and dynamic content for your audience.

## Host Configuration

```python
from chronocast import Host, OpenaiModels, AudioTools, WebTools

storyteller = Host(
    host_id="interactive_storyteller",
    role="Creative Storyteller",
    goal="Create engaging interactive stories",
    attributes="You are a charismatic storyteller who excels at creating immersive narratives and adapting to audience reactions",
    llm=OpenaiModels.gpt_4_turbo,
    tools={AudioTools.TextToSpeechTools, WebTools.exa_search}
)
```

### Core Properties

- **host_id**: A unique identifier for your Host
- **role**: The Host's primary role in the experience (e.g., "Storyteller", "Game Master", "Talk Show Host")
- **goal**: The Host's main objective when interacting with viewers
- **attributes**: Personality traits and characteristics that define the Host's behavior
- **llm**: The AI model powering the Host's intelligence
- **tools**: Set of capabilities available to the Host

## Host Types

### Storyteller
Perfect for creating interactive narratives, where the story adapts based on viewer choices:
```python
storyteller = Host(
    host_id="fantasy_storyteller",
    role="Fantasy Storyteller",
    goal="Create immersive fantasy adventures",
    attributes="Expert in fantasy lore, character voices, and dramatic narration",
    llm=OpenaiModels.gpt_4_turbo,
    tools={
        AudioTools.TextToSpeechTools,
        AudioTools.SoundEffects,
        WebTools.image_generation
    }
)
```

### Game Master
Ideal for running interactive games and RPG sessions:
```python
game_master = Host(
    host_id="rpg_master",
    role="RPG Game Master",
    goal="Run engaging tabletop RPG sessions",
    attributes="Expert in game rules, storytelling, and player engagement",
    llm=AnthropicModels.claude_3_opus,
    tools={
        AudioTools.TextToSpeechTools,
        AudioTools.SoundEffects,
        WebTools.image_generation,
        GameTools.dice_roller
    }
)
```

### Talk Show Host
Perfect for interactive interviews and discussions:
```python
talk_show_host = Host(
    host_id="tech_talk_host",
    role="Technology Talk Show Host",
    goal="Host engaging tech discussions",
    attributes="Knowledgeable about technology, great at interviewing and audience engagement",
    llm=OpenaiModels.gpt_4_turbo,
    tools={
        AudioTools.TextToSpeechTools,
        WebTools.exa_search,
        WebTools.news_search
    }
)
```

## Host Capabilities

### Tool Integration
Hosts can be equipped with various tools to enhance their capabilities:

```python
from chronocast import Host, AudioTools, WebTools, VisualizationTools

host = Host(
    host_id="multimedia_creator",
    role="Creative Content Creator",
    goal="Create engaging multimedia content",
    tools={
        AudioTools.TextToSpeechTools,    # Voice generation
        AudioTools.SoundEffects,         # Sound effects
        WebTools.image_generation,        # Image creation
        VisualizationTools.scene_render   # Scene visualization
    }
)
```

### Real-Time Adaptation
Hosts can dynamically adapt to viewer interactions:

```python
experience = Experience.create(
    host=host,
    adaptation_settings={
        "response_style": "dynamic",
        "personality_adaptation": True,
        "content_pacing": "adaptive",
        "interaction_memory": True
    }
)
```

### Multi-Modal Interaction
Hosts can engage with viewers across different modalities:

```python
experience = Experience.create(
    host=host,
    interaction_modes={
        "voice": True,
        "text": True,
        "visuals": True,
        "choices": True
    }
)
```

## Best Practices

1. **Clear Role Definition**: Give your Host a well-defined role and goal
2. **Personality Consistency**: Use the attributes field to maintain consistent personality
3. **Appropriate Tools**: Equip your Host with tools that match their role
4. **Performance Optimization**: Choose the right LLM based on your needs
5. **Interactive Design**: Configure your Host for engaging viewer interactions

## Next Steps

- [Build an Interactive Experience](tasks.md)
- [Explore Available Tools](tools/index.md)
- [View Example Hosts](https://docs.chronocast.xyz/examples/hosts)
