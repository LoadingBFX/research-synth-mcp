"""
@author: bfx
@version: 1.0.0
@file: openai_agent.py.py
@time: 4/25/25 15:17
"""
# agents/openai_agent.py
import os
from typing import Dict, List, Any, Optional
from openai import OpenAI
from mcp.protocol import MCPMessage
from agents.base import BaseAgent


class OpenAIAgent(BaseAgent):
    """Agent implementation for OpenAI models, optionally using LiteLLM proxy"""

    def __init__(
            self,
            agent_id: str,
            name: str,
            role: str,
            api_key: str,
            model: str,
            base_url: Optional[str] = None,
            system_prompt: Optional[str] = None
    ):
        super().__init__(
            agent_id=agent_id,
            name=name,
            role=role,
            api_key=api_key,
            model=model,
            api_url=base_url,  # Store base_url in api_url for consistency
            system_prompt=system_prompt
        )

        # Use LiteLLM base URL if provided, otherwise use default OpenAI URL
        client_args = {"api_key": api_key}
        if base_url:
            client_args["base_url"] = base_url

        # Initialize OpenAI client
        self.client = OpenAI(**client_args)

    def format_messages_for_api(self) -> List[Dict[str, Any]]:
        """Format messages for OpenAI API"""
        formatted_messages = []

        for msg in self.messages:
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })

        return formatted_messages

    def generate_response(self, prompt: Optional[str] = None) -> MCPMessage:
        """Generate a response using OpenAI API"""
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
            # Call OpenAI API
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
            error_msg = f"Error in OpenAI API call: {str(e)}"
            print(error_msg)
            # Return error as message
            error_response = self.create_message(content=error_msg)
            self.add_message(error_response)
            return error_response


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    import pathlib

    # Find the root directory (where .env should be)
    current_dir = pathlib.Path(__file__).parent
    root_dir = current_dir.parent  # Go up one level from /agents to the root

    # Load the .env file from the root directory
    load_dotenv(root_dir / ".env")
    # Load API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        exit(1)

    # Get optional LiteLLM base URL if available
    base_url = os.environ.get("LITELLM_BASE_URL")

    # Create test agent
    agent = OpenAIAgent(
        agent_id="test_agent",
        name="TestAgent",
        role="assistant",
        api_key=api_key,
        model="gpt-4o",  # Use a less expensive model for testing
        base_url=base_url,
        system_prompt="You are a helpful assistant designed to test the OpenAIAgent implementation."
    )

    # Test with a simple prompt
    test_prompt = "Tell me a short joke about programming."
    print(f"Testing agent with prompt: {test_prompt}")

    # Generate response
    response = agent.generate_response(test_prompt)

    # Print response
    print("\nResponse:")
    print(f"Message ID: {response.message_id}")
    print(f"References: {response.references}")
    print(f"Content: {response.content}")

    # Test conversation continuity
    follow_up_prompt = "Explain why that joke is funny."
    print(f"\nTesting follow-up prompt: {follow_up_prompt}")

    # Generate response to follow-up
    follow_up_response = agent.generate_response(follow_up_prompt)

    # Print follow-up response
    print("\nFollow-up Response:")
    print(f"Message ID: {follow_up_response.message_id}")
    print(f"References: {follow_up_response.references}")
    print(f"Content: {follow_up_response.content}")

    # Print conversation history
    print("\nFull Conversation History:")
    for i, msg in enumerate(agent.messages):
        print(f"{i + 1}. [{msg.role}] {msg.content[:50]}... (ID: {msg.message_id})")