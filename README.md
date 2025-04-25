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
- **Flexible LLM Integration**: Works with different LLM providers (OpenAI, Anthropic, etc.)
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
│  OpenAI API   │       │ Anthropic API │
└───────────────┘       └───────────────┘
```

## Installation

### Prerequisites

- Python 3.8+
- API keys for at least one LLM provider (OpenAI, Anthropic, etc.)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/research-synth-mcp.git
   cd research-synth-mcp
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

## Usage

### Basic Example

```bash
# Run with a single query
python run.py --query "Research the impact of quantum computing on encryption standards" --turns 3 --output "quantum_research.json"
```

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
- OpenAI and Anthropic for providing powerful language models
- All contributors to this project

## Citation

If you use this code in your research, please cite:

```bibtex
@software{research_synth_mcp,
  author = {Fanxing Bu},
  title = {Research-Synth-MCP: A Multi-Agent System Using Model Context Protocol},
  year = {2025},
  url = {https://github.com/yourusername/research-synth-mcp}
}
```
