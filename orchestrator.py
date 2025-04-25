"""
@author: bfx
@version: 1.0.0
@file: orchestrator.py.py
@time: 4/25/25 15:12
"""
# orchestrator.py
import json
import time
from typing import Dict, List, Any
from mcp.protocol import MCPMessage
from agents.base import BaseAgent


class Orchestrator:
    """Manages communication flow between agents"""

    def __init__(self, agents: List[BaseAgent]):
        self.agents = {agent.agent_id: agent for agent in agents}
        self.conversation_history: List[MCPMessage] = []

    def _record_message(self, message: MCPMessage):
        """Add message to conversation history"""
        self.conversation_history.append(message)

    def send_message(self, from_agent_id: str, to_agent_id: str, message: MCPMessage):
        """Send message from one agent to another"""
        # Record the message
        self._record_message(message)

        # Add message to receiving agent's context
        to_agent = self.agents[to_agent_id]
        to_agent.add_message(message)

    def run_workflow(self, initial_query: str, max_turns: int = 3) -> List[Dict[str, Any]]:
        """Run the multi-agent workflow for a set number of turns"""
        print(f"Starting workflow with query: {initial_query}")

        # Get agent IDs for convenience
        agent_ids = list(self.agents.keys())
        researcher_id = agent_ids[0]
        synthesizer_id = agent_ids[1]

        # Start with initial query to researcher
        researcher = self.agents[researcher_id]
        user_msg = MCPMessage(
            role="user",
            content=initial_query,
            agent_id="human",
        )
        researcher.add_message(user_msg)
        self._record_message(user_msg)

        print(f"\n[Human → {researcher.name}]: {initial_query}")

        # Run the workflow for specified turns
        for turn in range(max_turns):
            print(f"\n--- Turn {turn + 1} ---")

            # Researcher agent generates response
            print(f"\n[{researcher.name} thinking...]")
            research_response = researcher.generate_response()
            print(f"[{researcher.name}]: {research_response.content[:150]}...")

            # Send researcher's response to synthesizer
            synthesizer = self.agents[synthesizer_id]
            self.send_message(researcher_id, synthesizer_id, research_response)

            # Create prompt for synthesizer
            synth_prompt = f"Based on the research provided, please synthesize the key points and provide a critical analysis."
            synth_msg = MCPMessage(
                role="user",
                content=synth_prompt,
                agent_id="orchestrator",
                references=[research_response.message_id],
                metadata={"type": "instruction"}
            )
            synthesizer.add_message(synth_msg)
            self._record_message(synth_msg)

            # Synthesizer generates response
            print(f"\n[{synthesizer.name} thinking...]")
            synthesis_response = synthesizer.generate_response()
            print(f"[{synthesizer.name}]: {synthesis_response.content[:150]}...")

            # Send synthesizer's response back to researcher for next turn
            self.send_message(synthesizer_id, researcher_id, synthesis_response)

            # Update query for researcher's next turn
            if turn < max_turns - 1:
                followup_prompt = f"Consider the synthesis and critique above. Please investigate further on any gaps or areas that need more explanation."
                followup_msg = MCPMessage(
                    role="user",
                    content=followup_prompt,
                    agent_id="orchestrator",
                    references=[synthesis_response.message_id],
                    metadata={"type": "instruction"}
                )
                researcher.add_message(followup_msg)
                self._record_message(followup_msg)

        # Convert conversation history to simplified format for return
        formatted_history = []
        for msg in self.conversation_history:
            agent_name = "Human"
            if msg.agent_id in self.agents:
                agent_name = self.agents[msg.agent_id].name
            elif msg.agent_id == "orchestrator":
                agent_name = "Orchestrator"

            formatted_history.append({
                "agent": agent_name,
                "role": msg.role,
                "content": msg.content,
                "message_id": msg.message_id,
                "references": msg.references
            })

        return formatted_history

    def save_transcript(self, filename: str = "mcp_transcript.json"):
        """Save the conversation transcript to a file"""
        formatted_history = []
        for msg in self.conversation_history:
            agent_name = "Human"
            if msg.agent_id in self.agents:
                agent_name = self.agents[msg.agent_id].name
            elif msg.agent_id == "orchestrator":
                agent_name = "Orchestrator"

            formatted_history.append({
                "agent": agent_name,
                "role": msg.role,
                "content": msg.content,
                "message_id": msg.message_id,
                "references": msg.references,
                "timestamp": msg.timestamp
            })

        with open(filename, "w") as f:
            json.dump(formatted_history, f, indent=2)

        print(f"Transcript saved to {filename}")