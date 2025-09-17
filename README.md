# FastRTT Crew

Welcome to the FastRTT Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

This project requires [`uv`](https://docs.astral.sh/uv/) and [`crewai`](https://www.crewai.com/).

1. Clone and install dependencies

```bash
git clone https://github.com/lsc-sde/fastrtt/
cd fastrtt
uv sync
```
2. Setup environment variables

Copy `sample.env` to a new file called `.env` and fill in the necessary values.

3. Kickoff the crew

```bash
fastrtt
```

or

```bash
crewai run
```

## Understanding Your Crew

The FastRTT Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions of feedback regarding FastRTT, please reach out through [Github Issues](https://github.com/lsc-sde/fastrtt/issues) or directly to @vvcb.

For support, questions, or feedback regarding crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/crewAIInc/crewAI)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
