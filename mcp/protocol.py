"""
@author: bfx
@version: 1.0.0
@file: protocol.py.py
@time: 4/25/25 15:13
"""
# mcp/protocol.py
import time
import uuid
from typing import Dict, List, Any, Optional


class MCPMessage:
    """Implementation of a message following the Model Context Protocol"""

    def __init__(
            self,
            role: str,
            content: str,
            agent_id: str,
            message_id: Optional[str] = None,
            references: Optional[List[str]] = None,
            metadata: Optional[Dict[str, Any]] = None
    ):
        self.role = role
        self.content = content
        self.agent_id = agent_id
        self.message_id = message_id or f"msg_{uuid.uuid4().hex[:10]}"
        self.references = references or []
        self.metadata = metadata or {}
        self.timestamp = time.time()

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to MCP dictionary format"""
        return {
            "role": self.role,
            "content": self.content,
            "mcp": {
                "message_id": self.message_id,
                "agent_id": self.agent_id,
                "references": self.references,
                "metadata": self.metadata,
                "timestamp": self.timestamp
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPMessage':
        """Create message from dictionary"""
        mcp_data = data.get("mcp", {})

        return cls(
            role=data["role"],
            content=data["content"],
            agent_id=mcp_data.get("agent_id", "unknown"),
            message_id=mcp_data.get("message_id"),
            references=mcp_data.get("references", []),
            metadata=mcp_data.get("metadata", {})
        )