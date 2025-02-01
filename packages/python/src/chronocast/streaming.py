import json
from typing import List, Callable, Any
from datetime import datetime
from typing import Optional
from multiprocessing import Queue
from pydantic import BaseModel
from .experience import StreamTask
from .host import Host


class StreamInstruction(BaseModel):
    """
    Represents an instruction for creating a segment of an interactive streaming experience.
    
    This model defines how different segments of content should be created and how they
    relate to each other in the overall stream flow.
    """
    segment_id: str
    host_id: str
    instruction: str
    use_output_from: List[str] = []


class Stream:
    """
    Manages the flow of an interactive streaming experience by coordinating multiple AI hosts.
    
    This class enables seamless transitions between different segments of content, allowing
    hosts to build upon each other's outputs for a cohesive experience.
    """
    
    @staticmethod
    def stream_tool(*hosts: Host, tool_summaries: bool = False) -> Callable:
        """Returns the stream_tool function for managing interactive content flow."""

        def create_stream_tool(hosts: List[Any], tool_summaries: bool) -> Callable:
            host_map = {host.host_id: host for host in hosts}
            host_tools = {
                host.host_id: [tool.__name__ for tool in getattr(host, "tools", []) or []]
                for host in hosts
            }

            # Format available hosts string with their tools
            available_hosts = "\n            ".join(
                f"- {host_id}\n    ({host_id}'s tools: {', '.join(host_tools[host_id] or ['No tools'])})"
                for host_id in sorted(host_map.keys())
            )

            async def stream_tool(
                segments: List, event_queue: Optional[Queue] = None, **kwargs
            ) -> Any:
                print(f"[STREAM] Starting stream with {len(segments)} segments")

                # Add max iteration limits
                MAX_HOST_ITERATIONS = 3  # Maximum times a host can attempt to complete a segment

                messages = kwargs.get("messages", [])
                current_time = datetime.now().isoformat()

                # Track host iterations
                host_call_counts = {}  # Track {host_id: count}

                # Standardized initial delegation message
                delegation_start = {
                    "type": "delegation",
                    "role": "assistant",
                    "name": "delegation",
                    "content": f"Starting multi-agent flow with {len(segments)} segments",
                    "segments": [segment.get("segment_id") for segment in segments],
                    "timestamp": current_time,
                }

                # Add to messages and forward to callback
                if messages is not None:
                    messages.append(delegation_start)
                if kwargs.get("callback"):
                    await kwargs["callback"](delegation_start)

                if not segments or not isinstance(segments, list):
                    raise ValueError(
                        f"segments must be a non-empty list of segment dictionaries. Received: {segments}"
                    )

                all_results = {}
                sent_messages = set()

                for instruction_item in segments:
                    # Convert dict to StreamInstruction model
                    segment = StreamInstruction.model_validate(instruction_item)

                    target_host = host_map.get(segment.host_id)
                    print(
                        f"[STREAM] Processing segment '{segment.segment_id}' with host '{segment.host_id}'"
                    )

                    if not target_host:
                        print(
                            f"[STREAM] Warning: Host {segment.host_id} not found. Available hosts: {list(host_map.keys())}"
                        )
                        continue

                    # Track host iterations
                    host_call_counts[segment.host_id] = host_call_counts.get(segment.host_id, 0) + 1
                    if host_call_counts[segment.host_id] > MAX_HOST_ITERATIONS:
                        print(
                            f"[STREAM] Warning: Host {segment.host_id} exceeded maximum iterations"
                        )
                        continue

                    # Initialize messages with system message for this specific host
                    messages = [
                        {
                            "role": "system",
                            "content": (
                                f"You are {target_host.role}. "
                                f"Your goal is {target_host.goal}"
                                f"{' Your attributes are: ' + target_host.attributes if target_host.attributes and target_host.attributes.strip() else ''}"
                            ).strip(),
                        }
                    ]

                    print(f"\n[STREAM] Starting segment for host: {segment.host_id}")
                    instruction_text = segment.instruction + (
                        "\n\nUse the following information from previous segments:\n\n"
                        + "\n\n".join(
                            f"Results from segment '{dep_id}':\n{all_results[dep_id]}"
                            for dep_id in segment.use_output_from
                            if dep_id in all_results
                        )
                        if segment.use_output_from
                        else ""
                    )

                    async def nested_callback(result):
                        if isinstance(result, dict) and result.get("tool"):
                            current_time = datetime.now().isoformat()

                            # Ensure any existing timestamp is serializable
                            if "timestamp" in result and isinstance(result["timestamp"], datetime):
                                result["timestamp"] = result["timestamp"].isoformat()

                            # Standardize message format for all delegation-related events
                            if result.get("type") in ["delegation_result", "final_response"]:
                                message = {
                                    "type": "delegation_result",
                                    "role": "delegation",
                                    "name": target_host.host_id,
                                    "content": result.get("content", ""),
                                    "conducted_segment_id": segment.segment_id,
                                    "timestamp": current_time,
                                }

                                # Add to messages if available
                                if messages is not None:
                                    messages.append(message)

                                # Forward to parent callback
                                if kwargs.get("callback"):
                                    await kwargs["callback"](message)

                            # Handle other event types (tool calls etc)
                            else:
                                # Add role field for tool calls
                                if result.get("type") == "tool_call":
                                    result["role"] = (
                                        "delegation"
                                        if result.get("tool") == "stream_tool"
                                        else "function"
                                    )

                                result.update(
                                    {
                                        "host_id": target_host.host_id,
                                        "conducted_segment_id": segment.segment_id,
                                        "timestamp": current_time,
                                    }
                                )
                                if kwargs.get("callback"):
                                    # Ensure result is JSON serializable
                                    result_to_send = json.loads(json.dumps(result, default=str))
                                    await kwargs["callback"](result_to_send)

                            # Create unique signature based on event type
                            msg_signature = f"{result.get('type')}:{result.get('content')}:{result.get('host_id')}"

                            # Add specific signatures for different event types
                            if result.get("type") == "tool_call":
                                msg_signature += (
                                    f":{result.get('tool')}:{json.dumps(result.get('params', {}))}"
                                )
                                # print(f"[DELEGATION DEBUG] Tool call: {result.get('tool')}")
                            elif result.get("type") == "tool_result":
                                msg_signature += f":{result.get('tool')}"
                                # print(f"[DELEGATION DEBUG] Tool result received")
                            elif result.get("type") == "delegation_result":
                                msg_signature += f":delegation:{result.get('conducted_segment_id')}"
                                msg_signature += f":delegation:{result.get('conducted_task_id')}"
                                # print(f"[DELEGATION DEBUG] Conductor result received for task: {result.get('conducted_task_id')}")

                            # Send to event queue if available
                            if event_queue:
                                event_queue.put(result)
                                sent_messages.add(msg_signature)

                    task_result = await Task.create(
                        agent=target_agent,
                        instruction=instruction_text,
                        callback=nested_callback,
                        event_queue=event_queue,
                        messages=messages,
                        tool_summaries=tool_summaries,
                    )

                    # Include context in the result
                    context = "\n\n".join(
                        f"Results from task '{dep_id}':\n{all_results[dep_id]}"
                        for dep_id in task.use_output_from
                        if dep_id in all_results
                    )
                    all_results[task.task_id] = (
                        f"{context}\n\n{task_result}" if context else task_result
                    )

                # Return the final combined results
                return "\n\n".join(
                    f"Task '{task_id}':\n"
                    f"Instruction: {next((item['instruction'] for item in tasks if item['task_id'] == task_id), '')}\n"
                    f"Result: {result}"
                    for task_id, result in all_results.items()
                )

            conduct_tool.__name__ = "conduct_tool"
            conduct_tool.__doc__ = f"""Tool function to orchestrate multiple agents in a single, coordinated multi-agent flow. Tasks should be submitted in a single list, and they will be executed in the order they are submitted. Do not make separate calls to the tool.
            Consider the flow of information through the tasks when writing your orchestration: **if the final task depends on the output of an earlier task, you must include the task_id of the task it depends on in the "use_output_from" field**.
            Your team members can handle multiple similar tasks in one instruction.
            For example, if you want a travel agent to find flights and a spreadsheet agent to create a spreadsheet with the flight options, you *MUST* include the task_id of the travel related task in the "use_output_from" field of the spreadsheet agent's task.
            Your instruction should be an extensive and well engineered prompt instruction for the agent. Don't just issue a simple instruction string; tell it what to do and achieve, and what its final response should be.

            Available Agents (to be used as agent_id in the conduct_tool instruction):
            {available_agents}

            Tool name: conduct_tool
            
            Args:
                tasks (List[dict]): List of task objects with format:
                    [
                        {{
                            "task_id": str,  # Unique identifier for this task (e.g., "task_1", "extract_data")
                            "agent_id": str,  # ID of the agent to use (must be in available_ids, case-sensitive)
                            "instruction": str,  # Instruction for the agent (should be a comprehensive prompt)
                            "use_output_from": List[str] = []  # List of task_ids to use results from
                        }},
                        {{
                            "task_id": str,  # Unique identifier for this task (e.g., "task_2" or "finalize_report")
                            "agent_id": str,  # ID of the agent to use
                            "instruction": str,  # Instruction for the agent
                            "use_output_from": List[str] = []  # Can reference previous task_ids
                        }},
                        ...  # Additional tasks can be added as needed
                    ]

            Returns:
                str: A formatted string containing the results of all tasks, with each task's instruction and result clearly labeled.
            """
            return conduct_tool

        return create_conduct_tool(list(agents), tool_summaries)


class Compose:
    @staticmethod
    def multicompose_tool(*agents: Agent) -> Callable:
        """Returns the composition tool function directly."""

        def create_composition_tool(agents: List[Agent]) -> Callable:
            agent_map = {agent.agent_id: agent for agent in agents}
            agent_tools = {
                agent.agent_id: [tool.__name__ for tool in getattr(agent, "tools", []) or []]
                for agent in agents
            }
            # Format available agents string
            available_agents = "\n            ".join(
                f"- {agent_id}\n    ({agent_id}'s tools: {', '.join(agent_tools[agent_id] or ['No tools'])})"
                for agent_id in sorted(agent_map.keys())
            )

            async def composition_tool(
                goal: str, event_queue: Optional[Queue] = None, **kwargs
            ) -> Any:
                # KEEP: Create composer agent instance with all these fields
                composer_agent = Agent(
                    agent_id="composer",
                    role="Composer",
                    goal="To create structured, efficient plans for multi-agent task execution",
                    attributes="""You are a thoughtful composer who excels at planning and structuring complex tasks. Like a musical composer, you understand how different elements must come together harmoniously to create a complete work. You carefully consider the capabilities of each agent as if they were musicians in your orchestra, knowing when to leverage their individual strengths and how to combine them effectively.
You approach planning with both precision and creativity, ensuring each task flows naturally into the next while maintaining clear dependencies and relationships. Your plans account for the flow of information between tasks.
You create plans that are both comprehensive and elegant, with a natural rhythm and flow to their execution. You consider not just what needs to be done, but how it should be orchestrated for maximum efficiency and effectiveness. Each plan you create includes clear task breakdowns, thoughtful agent assignments, explicit dependencies, and well-defined success criteria. You express these elements in clear, narrative form that guides the execution while maintaining flexibility for dynamic adjustments as needed.
Your responses take the form of well-structured plans that read like a score, guiding each agent through their part while maintaining the coherence of the whole. You balance detail with clarity, ensuring your plans are thorough without becoming overwhelming. You maintain awareness of the overall goal while carefully considering each component.""",
                    llm=next(iter(agents)).llm,
                )

                # KEEP: Initialize messages array with BOTH system and user messages
                messages = [
                    {
                        "role": "system",
                        "content": (
                            f"You are {composer_agent.role}. "
                            f"Your goal is {composer_agent.goal}"
                            f"{' Your attributes are: ' + composer_agent.attributes if composer_agent.attributes and composer_agent.attributes.strip() else ''}"
                        ).strip(),
                    },
                    {
                        "role": "user",
                        "content": f"""Create a detailed plan for achieving this goal: {goal}
                    
Available agents and their capabilities:
{chr(10).join(f'- {agent.agent_id}: {agent.goal}' for agent in agents)}

Your plan should outline:
1. The sequence of tasks needed
2. Which agent should handle each task
3. What information flows between tasks""",
                    },
                ]

                try:
                    # KEEP: All these parameters to Task.create()
                    task_result = await Task.create(
                        agent=composer_agent,
                        instruction=f"Create a detailed plan for achieving this goal: {goal}",
                        callback=kwargs.get("callback"),
                        event_queue=event_queue,
                        messages=messages,
                    )
                    return task_result
                except Exception as e:
                    print(f"[COMPOSITION ERROR] Failed to create task: {str(e)}")
                    raise

            composition_tool.__name__ = "composition_flow"
            composition_tool.__doc__ = f"""Tool function to create a detailed plan for executing a sequence of tasks across multiple agents.

            This tool should be used BEFORE delegating tasks to create a comprehensive plan. It helps structure and organize how tasks should flow between agents.
            The tool will analyze the tasks and dependencies to create an optimal execution plan, considering:
            - What information each task needs
            - Which tasks depend on outputs from other tasks
            - How to sequence the tasks efficiently
            - What specific instructions each agent needs

            The plan can then be used to guide the actual task delegation and execution.

            Available Agents:
            {available_agents}

            Args:
                goal (str): The goal of the composition.

            Returns:
                str: A detailed execution plan to assist in your orchestration.
            """
            return composition_tool

        return create_composition_tool(list(agents))
