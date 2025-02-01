from datetime import datetime
import base64
import re
import json
from typing import Union


class StreamHelpers:
    """
    Helper utilities for managing interactive streaming experiences.
    
    This class provides utility functions for handling common tasks in content
    creation and streaming, such as managing conversation history, processing
    media assets, and parsing responses.
    """
    
    @staticmethod
    def update_stream_history(history, role, content):
        """
        Format and record an interaction in the streaming experience history.

        Args:
            history (list): The current stream history as a list of formatted messages.
            role (str): The role of the participant (e.g., "Host" or "Viewer").
            content (str): The message or interaction content.

        Returns:
            list: Updated stream history with timestamp and formatting.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {role}: {content}"
        history.append(formatted_message)
        return history

    @staticmethod
    def media_to_base64(media_path: str, scale_factor: float = 0.5) -> str:
        """
        Convert media content to a base64-encoded string for streaming.

        Args:
            media_path (str): The path to the media file (image, audio, etc.).
            scale_factor (float, optional): Factor to scale media dimensions. Defaults to 0.5.

        Returns:
            str: Base64-encoded string representation of the (optionally processed) media.

        Raises:
            IOError: If there's an error opening or processing the media file.
        """
        import numpy as np
        from io import BytesIO

        with open(media_path, "rb") as media_file:
            data = np.frombuffer(media_file.read(), dtype=np.uint8)
            data = data.reshape((-1, 3))  # Assuming 3 channels (RGB)
            processed_data = data[:: int(1 / scale_factor)]
            
            # Convert back to bytes
            buffer = BytesIO()
            np.save(buffer, processed_data)
            return base64.b64encode(buffer.getvalue()).decode()

    @staticmethod
    def parse_stream_response(response: Union[str, dict]) -> dict:
        """
        Parse and validate responses from AI hosts or stream processors.

        This method handles various response formats and ensures they are
        properly structured for the streaming experience.

        Args:
            response (Union[str, dict]): The raw response from an AI host or processor.

        Returns:
            dict: Properly formatted response data.

        Raises:
            ValueError: If the response cannot be parsed or is invalid.
        """
        if isinstance(response, dict):
            return response

        try:
            # Remove any markdown code block formatting
            if response.startswith("```") and response.endswith("```"):
                response = "\n".join(response.split("\n")[1:-1])

            # Try to parse as JSON
            return json.loads(response)
        except json.JSONDecodeError as e:
            # Try to extract JSON from text
            json_pattern = r"\{(?:[^{}]|(?:\{[^{}]*\}))*\}"
            matches = re.finditer(json_pattern, response, re.DOTALL)
            
            for match in matches:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    continue

            raise ValueError(f"Could not parse stream response: {str(e)}")
