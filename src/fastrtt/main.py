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
    clinic_letter = """Dear Doctor,

Thank you for your referral. I saw this pleasant 70 year old man in my clinic today.

He presents with a 1 year history of a lump in his right groin.
History is typical for a right inguinal hernia. This causes minimal symptoms.

He has had a myocardial infarction 5 years ago and has congestive heart failure.
His exercise tolerance is limited to 50 yards.

Clinical examination confirmed a easily reducible right inguinal hernia.

In view of his comorbidities and the lack of symptoms, I have advised against surgery.
He is in agreement with this. I have not made any further arrangements to see him again but will be happy to do so should he become more symptomatic.

Kind regards.

Mr. Smith """
    inputs = {"clinic_letter": clinic_letter}

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
