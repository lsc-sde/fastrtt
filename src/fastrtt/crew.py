from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

json_knowledge = JSONKnowledgeSource(
    file_paths=["rtt-guidance-feb-25_sections.json"],
)


@CrewBase
class Fastrtt:
    """Fastrtt crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    mcp_server_params = [
        StdioServerParameters(
            command="uv",
            args=["run", "fastrtt_mcp"],
        )
    ]

    @agent
    def data_retrieval_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["data_retrieval_agent"],  # type: ignore[index]
            verbose=False,
            tools=self.get_mcp_tools(),
        )

    @agent
    def data_intent_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["data_intent_agent"],  # type: ignore[index]
            verbose=False,
            # knowledge_sources=[json_knowledge],  # Temporarily disabled
        )

    @agent
    def clock_stop_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["clock_stop_analyst"],  # type: ignore[index]
            verbose=False,
            # knowledge_sources=[json_knowledge],  # Temporarily disabled
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def data_retrieval_task(self) -> Task:
        return Task(
            config=self.tasks_config["data_retrieval_task"],  # type: ignore[index]
        )

    @task
    def data_intent_task(self) -> Task:
        return Task(
            config=self.tasks_config["data_intent_task"],  # type: ignore[index]
        )

    @task
    def clock_stop_task(self) -> Task:
        return Task(
            config=self.tasks_config["clock_stop_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Fastrtt crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # knowledge_sources=[json_knowledge],
            # embedder={
            #     "provider": "ollama",
            #     "config": {
            #         "model": "nomic-embed-text:latest",
            #         "url": "http://localhost:11434/api/embed",
            #     },
            # },
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
