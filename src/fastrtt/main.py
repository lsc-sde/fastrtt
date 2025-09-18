#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from fastrtt.crew import Fastrtt
from fastrtt.otel import langfuse

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    person_id = "3695604"
    start_date = "2025-01-01"
    end_date = "2025-12-31"

    inputs = {"person_id": person_id, "start_date": start_date, "end_date": end_date}

    with langfuse.start_as_current_span(name="Run_FastRTT"):
        try:
            Fastrtt().crew().kickoff(inputs=inputs)
        except Exception as e:
            raise Exception(f"An error occurred while running the crew: {e}")
    langfuse.flush()


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "AI LLMs", "current_year": str(datetime.now().year)}
    try:
        Fastrtt().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Fastrtt().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"topic": "AI LLMs", "current_year": str(datetime.now().year)}

    try:
        Fastrtt().crew().test(
            n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
