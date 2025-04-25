# Research-Synth-MCP

A multi-agent AI system implementing the Model Context Protocol (MCP) for autonomous collaborative research and analysis.

## Overview

Research-Synth-MCP demonstrates the power of multi-agent collaboration through a specialized implementation of the Model Context Protocol. The system orchestrates two AI agents with distinct, complementary roles to work together on complex research tasks:

1. **ResearchBot**: Gathers comprehensive information on a given topic, covering multiple perspectives and identifying relevant facts
2. **SynthBot**: Analyzes, synthesizes, and critically evaluates the information provided by the researcher

The system enables these agents to collaborate with minimal human intervention after the initial query, creating a coherent research workflow that progressively refines information across multiple turns.

## Key Features

- **Full MCP Implementation**: Complete implementation of the Model Context Protocol with message IDs, reference chains, and metadata
- **Specialized Agent Roles**: Distinct, complementary capabilities for information gathering and synthesis
- **Context Preservation**: Maintains conversation history with reference tracking to build on previous exchanges
- **Multi-Turn Dialogue**: Supports iterative refinement through structured conversation sequences
- **Minimal Human Intervention**: Autonomous research flow after initial query
- **Flexible LLM Integration**: Works with different LLM providers (Groq, OpenAI, etc.)
- **Transcript Generation**: Exports complete conversation history in structured format

## Architecture

The system architecture consists of four main components:

1. **MCP Protocol Layer**: Handles message formatting, reference chains, and metadata
2. **Agent Layer**: Implements specialized agents with different roles and capabilities
3. **Orchestration Layer**: Manages workflow, message routing, and turn-taking
4. **Interface Layer**: Handles input/output and provides human interaction points

```
┌─────────────────────────────────────────┐
│               User Query                │
└───────────────────┬─────────────────────┘
                    ▼
┌─────────────────────────────────────────┐
│            Orchestrator                 │
└───────┬─────────────────────────┬───────┘
        │                         │
        ▼                         ▼
┌───────────────┐       ┌───────────────┐
│  ResearchBot  │◄─────►│   SynthBot    │
└───────┬───────┘       └───────┬───────┘
        │                       │
        ▼                       ▼
┌───────────────┐       ┌───────────────┐
│   Groq API    │       │  OpenAI API   │
└───────────────┘       └───────────────┘
```

## Installation

### Prerequisites

- Python 3.8 or newer
- API key for either Groq or OpenAI (or both, for maximum flexibility)
- Optional: LiteLLM proxy URL for OpenAI (for additional routing options)

### Setup

1. Clone the repository and set up your environment:
```bash
# Clone the repository
git clone https://github.com/LoadingBFX/research-synth-mcp.git
cd research-synth-mcp

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

2. API Key Setup
Create a `.env` file in the project root to store your API keys:
```
# Add one or both API keys depending on which services you plan to use
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Add LiteLLM base URL for OpenAI routing
LITELLM_BASE_URL=your_litellm_proxy_url_here
```

### Getting API Keys

#### Groq API Key (Free Option)
Groq currently offers free API access to their hosted models, including Llama 3:

1. Create an account at [console.groq.com](https://console.groq.com)
2. Go to the "API Keys" section in your account settings
3. Create a new API key and copy it
4. Paste it into your `.env` file

#### OpenAI API Key (Paid Option)
To use OpenAI models:

1. Create an account at [platform.openai.com](https://platform.openai.com)
2. Set up billing in your account settings
3. Go to the "API Keys" section and create a new secret key
4. Copy the key and paste it into your `.env` file

#### Setting Up LiteLLM Proxy (Optional)
You can use LiteLLM as a proxy to route requests to OpenAI models. This is helpful for:

- Centralizing API key management
- Adding rate limiting and quotas
- Routing to different model providers with the same interface

To set up LiteLLM:

1. Install LiteLLM: `pip install litellm`
2. Run LiteLLM as a proxy server: `litellm --model gpt-3.5-turbo`
3. Set the proxy URL in your `.env` file: `LITELLM_BASE_URL=http://localhost:4000`

For more advanced LiteLLM proxy configurations, refer to the LiteLLM documentation.

## Available Models

### Groq Models
- `llama3-8b-8192`: Smaller, faster Llama 3 model
- `llama3-70b-8192`: Larger, more capable Llama 3 model (recommended)
- `mixtral-8x7b-32768`: Mixtral model with large context window

### OpenAI Models
- `gpt-3.5-turbo`: Fast, cost-effective model
- `gpt-4o`: High-quality reasoning model with vision capabilities
- `gpt-4-turbo`: Powerful model with large context window

## Usage

### Basic Example

```bash
# Run with a single query
python run.py --query "Research the impact of quantum computing on encryption standards" --turns 3 --output "quantum_research.json"
```

### Configuration Options

The system allows you to mix and match different agent types and models for both the researcher and synthesizer roles.

#### Using Groq for Both Agents (Free)
```bash
python run.py --query "Research the impact of quantum computing on encryption standards" --researcher groq --synthesizer groq
```

#### Using OpenAI for Both Agents (Paid)
```bash
python run.py --query "Research the impact of quantum computing on encryption standards" --researcher openai --synthesizer openai
```

#### Using OpenAI with LiteLLM Proxy
```bash
# Make sure LITELLM_BASE_URL is set in your .env file
python run.py --query "Research the impact of quantum computing on encryption standards" --researcher openai --synthesizer openai
```

#### Using a Mixed Approach
You can also combine different providers for different roles:
```bash
python run.py --query "Research the impact of quantum computing on encryption standards" --researcher groq --researcher-model llama3-70b-8192 --synthesizer openai --synthesizer-model gpt-4o
```

### Command Line Options

- `--query`: The research question (required)
- `--turns`: Number of conversation turns (default: 3)
- `--output`: Output file path for transcript (default: mcp_transcript.json)
- `--researcher`: LLM provider for researcher agent (choices: "groq", "openai", default: "groq")
- `--researcher-model`: Specific model for researcher (if not specified, defaults to llama3-70b-8192 for Groq and gpt-4o for OpenAI)
- `--synthesizer`: LLM provider for synthesizer agent (choices: "groq", "openai", default: "groq")
- `--synthesizer-model`: Specific model for synthesizer (if not specified, defaults to llama3-70b-8192 for Groq and gpt-4o for OpenAI)

### Advanced Configuration

For more complex usage, you can modify the agent configurations in the `run.py` file:

```python
# Create custom researcher agent
researcher = OpenAIAgent(
    agent_id="researcher_1",
    name="CustomResearcher",
    role="information_gatherer",
    api_key=os.environ.get("OPENAI_API_KEY"),
    model="gpt-4",
    api_url="https://api.openai.com/v1/chat/completions",
    system_prompt="""Your custom prompt here"""
)
```

### Sample Output

The system generates a structured JSON transcript that shows the full conversation history with MCP metadata:

```json
[
  {
    "agent": "Human",
    "role": "user",
    "content": "Research the impact of quantum computing on encryption standards",
    "message_id": "msg_1682594371",
    "references": []
  },
  {
    "agent": "ResearchBot",
    "role": "assistant",
    "content": "I've researched the current state of quantum computing's impact on encryption standards. Here are my findings...",
    "message_id": "msg_1682594382",
    "references": ["msg_1682594371"]
  },
  ...
]
```
Terminal output will also show the progress of the research and synthesis process, including the turn-by-turn dialogue between the agents.
```bash
python run.py --query "Research the impact of quantum computing on encryption standards" --researcher openai --synthesizer groq
Starting research on: Research the impact of quantum computing on encryption standards
Researcher: openai (gpt-4o)
Using LiteLLM as proxy for researcher
Synthesizer: groq (llama3-70b-8192)
Starting workflow with query: Research the impact of quantum computing on encryption standards

[Human → ResearchBot]: Research the impact of quantum computing on encryption standards

--- Turn 1 ---

[ResearchBot thinking...]
[ResearchBot]: Quantum computing is poised to have a significant impact on encryption standards, as it introduces both challenges and opportunities in the field of c...

[SynthBot thinking...]
[SynthBot]: **Synthesis of Key Points:**

1. Quantum computing poses a significant threat to current encryption standards, particularly RSA and ECC, due to Shor's...

--- Turn 2 ---

[ResearchBot thinking...]
[ResearchBot]: To address the identified gaps and areas requiring further explanation, let's delve deeper into the following topics:

### Detailed Analysis of Candid...

[SynthBot thinking...]
[SynthBot]: **Synthesis of Key Points:**

1. Post-quantum cryptography is essential to mitigate the threat of quantum computers breaking current encryption standa...

--- Turn 3 ---

[ResearchBot thinking...]
[ResearchBot]: To address the identified gaps and areas requiring further explanation, let's focus on a more detailed analysis of the strengths and weaknesses of pos...

[SynthBot thinking...]
[SynthBot]: **Synthesis of Key Points:**

1. Post-quantum cryptography is essential to mitigate the threat of quantum computers breaking current encryption standa...

==================================================
FINAL RESEARCH RESULTS
==================================================

FINAL SYNTHESIS:
**Synthesis of Key Points:**

1. Post-quantum cryptography is essential to mitigate the threat of quantum computers breaking current encryption standards.
2. Lattice-based, hash-based, code-based, and multivariate polynomial cryptography are promising approaches to post-quantum cryptography, each with their strengths and weaknesses.
3. Transitioning to post-quantum cryptography involves significant cost implications, infrastructure overhauls, and timeline uncertainty.
4. The potential risks of not transitioning to post-quantum cryptography include national security breaches, data privacy compromises, and economic losses.
5. Governments and regulatory bodies play a crucial role in promoting the adoption of post-quantum cryptography standards through collaboration with industry and academia.

**Critical Analysis:**

**Strengths:**

1. The research provides a comprehensive overview of the importance of post-quantum cryptography and the various approaches being explored.
2. The discussion on the cost implications and potential risks of not transitioning to post-quantum cryptography is well-informed and highlights the need for urgent action.

**Weaknesses and Limitations:**

1. The research could benefit from a more detailed analysis of the strengths and weaknesses of each post-quantum cryptography approach.
2. The discussion on the cost implications of transitioning to post-quantum cryptography could be more detailed, including estimates and case studies.
3. The research does not explore the potential applications of post-quantum cryptography beyond encryption, including digital signatures and authentication.
4. The analysis could be strengthened by including more diverse perspectives from experts in the field, including those from industry and government.

**Suggestions for Further Investigation:**

1. Conduct a more detailed comparison of the strengths and weaknesses of lattice-based, hash-based, code-based, and multivariate polynomial cryptography approaches.
2. Investigate the cost implications of transitioning to post-quantum cryptography, including estimates and case studies.
3. Examine the potential risks and consequences of not transitioning to post-quantum cryptography, including the impact on national security and critical infrastructure.
4. Explore the role of government and regulatory bodies in promoting the adoption of post-quantum cryptography standards.
5. Investigate the potential applications of post-quantum cryptography beyond encryption, including digital signatures and authentication.

Overall, the research provides a solid foundation for understanding the importance of post-quantum cryptography and the various approaches being explored. However, further investigation is needed to address the gaps and limitations identified in this critical analysis.

Transcript saved to mcp_transcript.json
Research complete! Transcript saved to mcp_transcript.json

```

## Configuration Strategies

Here are some effective configurations to consider:

### Budget-Conscious Setup (All Free)
- Researcher: Groq with llama3-70b-8192
- Synthesizer: Groq with llama3-70b-8192
- Good quality results with no cost

### Maximum Quality Setup (Paid)
- Researcher: OpenAI with gpt-4o
- Synthesizer: OpenAI with gpt-4o
- Highest quality results but at a cost

### Balanced Approach (Hybrid)
- Researcher: Groq with llama3-70b-8192 (free)
- Synthesizer: OpenAI with gpt-4o (paid)
- This leverages the free Groq model for initial research and the more capable OpenAI model for critical analysis and synthesis, providing good value for money

### Self-Hosted Approach (with LiteLLM)
- Set up LiteLLM proxy on your server
- Configure LiteLLM to route to different model providers
- Use the same interface for all agents through the proxy

## Using LiteLLM for Additional Models

LiteLLM can proxy requests to many other models beyond OpenAI, including:
- Anthropic (Claude)
- Google (Gemini)
- Cohere
- Local models via Ollama

To use these additional models:
1. Set up LiteLLM with appropriate configurations
2. Update the OpenAI agent to use the correct model names through the proxy
3. Add the appropriate API keys to your LiteLLM configuration

## Project Structure

Ensure your project has the following structure:
```
research-synth-mcp/
├── .env                  # API key configuration
├── requirements.txt      # Dependencies
├── run.py                # Main script
├── mcp/
│   ├── __init__.py
│   └── protocol.py       # MCP implementation
├── agents/
│   ├── __init__.py
│   ├── base.py           # Base agent class
│   ├── openai_agent.py   # OpenAI implementation
│   └── groq_agent.py     # Groq implementation
└── orchestrator.py       # Orchestration logic
```

## Extending the System

### Adding New Agent Types

Create new agent classes by extending the `BaseAgent` class:

```python
class CriticAgent(BaseAgent):
    """Agent that evaluates information quality and reliability"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom initialization
```

### Implementing Memory Systems

The system can be extended with external memory to maintain context beyond context windows:

```python
# Example memory integration
memory = MCPMemory("research_memory.json")
memory.add_fact("RSA-2048 requires approximately 4,000 logical qubits to break", "researcher_1")
memory.save()
```

## Troubleshooting

- **API Key Issues**: Verify your API keys are correct and have the necessary permissions
- **Rate Limiting**: Both providers impose rate limits. If you encounter errors, consider adding delays between turns
- **LiteLLM Connection**: If using LiteLLM, make sure the proxy server is running and accessible
- **Model Availability**: If specific models become unavailable, try alternative models from the same provider
- **Installation Problems**: Make sure you have the latest versions of all required packages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Model Context Protocol community for specification development
- Groq and OpenAI for providing powerful language models
- All contributors to this project

## Citation

If you use this code in your research, please cite:

```bibtex
@software{research_synth_mcp,
  author = {Fanxing Bu},
  title = {Research-Synth-MCP: A Multi-Agent System Using Model Context Protocol},
  year = {2025},
  url = {https://github.com/LoadingBFX/research-synth-mcp}
}
```