"""
@author: bfx
@version: 1.0.0
@file: base.py.py
@time: 4/25/25 15:15
"""
# agents/base.py
import os
import requests
from typing import Dict, List, Any, Optional
from mcp.protocol import MCPMessage


class BaseAgent:
    """Base class for all agents in the system"""

    def __init__(
            self,
            agent_id: str,
            name: str,
            role: str,
            api_key: str,
            model: str,
            api_url: str,
            system_prompt: Optional[str] = None
    ):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.api_key = api_key
        self.model = model
        self.api_url = api_url
        self.system_prompt = system_prompt or f"You are {name}, an AI assistant with the role of {role}."
        self.messages: List[MCPMessage] = []

        # Initialize with system message
        self._add_system_message()

    def _add_system_message(self):
        """Add initial system message to context"""
        system_msg = MCPMessage(
            role="system",
            content=self.system_prompt,
            agent_id=self.agent_id,
            metadata={"type": "system_instruction"}
        )
        self.messages.append(system_msg)

    def add_message(self, message: MCPMessage):
        """Add a message to this agent's context"""
        self.messages.append(message)

    def create_message(self, content: str, role: str = "assistant", references: List[str] = None) -> MCPMessage:
        """Create a new message from this agent"""
        msg = MCPMessage(
            role=role,
            content=content,
            agent_id=self.agent_id,
            references=references,
            metadata={"agent_role": self.role}
        )
        return msg

    def format_messages_for_api(self) -> List[Dict[str, Any]]:
        """Format messages for API call - override in subclasses for specific APIs"""
        raise NotImplementedError("Subclasses must implement this method")

    def generate_response(self, prompt: Optional[str] = None) -> MCPMessage:
        """Generate a response using the model API - override in subclasses"""
        raise NotImplementedError("Subclasses must implement this method")