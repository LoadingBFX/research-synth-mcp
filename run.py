"""
@author: bfx
@version: 1.0.0
@file: run.py.py
@time: 4/25/25 15:12
"""
# run.py
import os
import argparse
from dotenv import load_dotenv
from agents.openai_agent import OpenAIAgent
from agents.groq_agent import GroqAgent
from agents.base import BaseAgent
from orchestrator import Orchestrator


def create_agent(agent_type: str, agent_id: str, name: str, role: str, model: str, system_prompt: str) -> BaseAgent:
    """Create an agent based on the specified type"""
    if agent_type.lower() == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("LITELLM_BASE_URL")

        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        return OpenAIAgent(
            agent_id=agent_id,
            name=name,
            role=role,
            api_key=api_key,
            model=model,
            base_url=base_url,
            system_prompt=system_prompt
        )
    elif agent_type.lower() == "groq":
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        return GroqAgent(
            agent_id=agent_id,
            name=name,
            role=role,
            api_key=api_key,
            model=model,
            system_prompt=system_prompt
        )
    else:
        raise ValueError(f"Unsupported agent type: {agent_type}")


def main():
    """Main function to run the MCP multi-agent system"""
    # Load environment variables
    load_dotenv()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run MCP Multi-Agent System")
    parser.add_argument("--query", type=str, required=True, help="Initial research query")
    parser.add_argument("--turns", type=int, default=3, help="Number of conversation turns")
    parser.add_argument("--output", type=str, default="mcp_transcript.json", help="Output file for transcript")
    parser.add_argument("--researcher", type=str, default="groq", choices=["groq", "openai"],
                        help="Researcher agent type")
    parser.add_argument("--researcher-model", type=str, help="Model for researcher agent")
    parser.add_argument("--synthesizer", type=str, default="groq", choices=["groq", "openai"],
                        help="Synthesizer agent type")
    parser.add_argument("--synthesizer-model", type=str, help="Model for synthesizer agent")
    args = parser.parse_args()

    # Set default models based on agent types if not specified
    if args.researcher_model is None:
        if args.researcher.lower() == "groq":
            args.researcher_model = "llama3-70b-8192"
        else:  # openai
            args.researcher_model = "gpt-4o"

    if args.synthesizer_model is None:
        if args.synthesizer.lower() == "groq":
            args.synthesizer_model = "llama3-70b-8192"
        else:  # openai
            args.synthesizer_model = "gpt-4o"

    # Create researcher agent
    researcher = create_agent(
        agent_type=args.researcher,
        agent_id="researcher_1",
        name="ResearchBot",
        role="information_gatherer",
        model=args.researcher_model,
        system_prompt="""You are ResearchBot, an AI research assistant.
Your role is to find and provide comprehensive information on given topics.
Focus on gathering facts, citing sources when possible, and covering different perspectives.
Organize information clearly and identify any gaps in knowledge.
"""
    )

    # Create synthesizer agent
    synthesizer = create_agent(
        agent_type=args.synthesizer,
        agent_id="synthesizer_1",
        name="SynthBot",
        role="critic_summarizer",
        model=args.synthesizer_model,
        system_prompt="""You are SynthBot, an AI synthesis and critique specialist.
Your role is to analyze information provided by a researcher, extract key insights,
identify patterns, evaluate the quality of information, highlight limitations,
and suggest areas for further investigation.
Be critical but constructive, and always strive for objectivity.
"""
    )

    # Set up orchestrator
    orchestrator = Orchestrator([researcher, synthesizer])

    # Print configuration
    print(f"Starting research on: {args.query}")
    print(f"Researcher: {args.researcher} ({args.researcher_model})")

    # Check if using LiteLLM for OpenAI
    if args.researcher.lower() == "openai" and os.environ.get("LITELLM_BASE_URL"):
        print(f"Using LiteLLM as proxy for researcher")

    print(f"Synthesizer: {args.synthesizer} ({args.synthesizer_model})")

    # Check if using LiteLLM for OpenAI
    if args.synthesizer.lower() == "openai" and os.environ.get("LITELLM_BASE_URL"):
        print(f"Using LiteLLM as proxy for synthesizer")

    # Run workflow
    results = orchestrator.run_workflow(args.query, max_turns=args.turns)
    print("\n" + "=" * 50)
    print("FINAL RESEARCH RESULTS")
    print("=" * 50)
    final_synth_message = None
    for message in reversed(results):
        if message['agent'] == 'SynthBot':
            final_synth_message = message
            break

    if final_synth_message:
        print(f"\nFINAL SYNTHESIS:\n{final_synth_message['content']}\n")
    else:
        print("\nNo synthesis found in results.\n")

    # Save transcript
    orchestrator.save_transcript(args.output)
    print(f"Research complete! Transcript saved to {args.output}")


if __name__ == "__main__":
    main()