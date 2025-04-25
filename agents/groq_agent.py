"""
@author: bfx
@version: 1.0.0
@file: groq_agent.py.py
@time: 4/25/25 15:35
"""
# agents/groq_agent.py
import os
from typing import Dict, List, Any, Optional
from groq import Groq
from mcp.protocol import MCPMessage
from agents.base import BaseAgent


class GroqAgent(BaseAgent):
    """Agent implementation for Groq models (Llama 3, etc.)"""

    def __init__(
            self,
            agent_id: str,
            name: str,
            role: str,
            api_key: str,
            model: str,
            system_prompt: Optional[str] = None
    ):
        super().__init__(
            agent_id=agent_id,
            name=name,
            role=role,
            api_key=api_key,
            model=model,
            api_url=None,  # Not needed for Groq client
            system_prompt=system_prompt
        )
        # Initialize Groq client
        self.client = Groq(api_key=api_key)

    def format_messages_for_api(self) -> List[Dict[str, Any]]:
        """Format messages for Groq API"""
        formatted_messages = []

        for msg in self.messages:
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })

        return formatted_messages

    def generate_response(self, prompt: Optional[str] = None) -> MCPMessage:
        """Generate a response using Groq API"""
        # If a new prompt is provided, add it as a user message
        if prompt:
            user_msg = MCPMessage(
                role="user",
                content=prompt,
                agent_id="human",
                metadata={"type": "query"}
            )
            self.add_message(user_msg)

        # Format messages for API
        formatted_messages = self.format_messages_for_api()

        try:
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=0.7,
                max_tokens=2048
            )

            # Extract response content
            content = response.choices[0].message.content

            # Create MCP message from response
            # Find message IDs to reference
            references = []
            if self.messages and self.messages[-1].role == "user":
                references.append(self.messages[-1].message_id)

            response_msg = self.create_message(content=content, references=references)
            self.add_message(response_msg)

            return response_msg

        except Exception as e:
            error_msg = f"Error in Groq API call: {str(e)}"
            print(error_msg)
            # Return error as message
            error_response = self.create_message(content=error_msg)
            self.add_message(error_response)
            return error_response