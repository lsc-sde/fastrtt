from langfuse import get_client
from openinference.instrumentation.crewai import CrewAIInstrumentor
from openinference.instrumentation.litellm import LiteLLMInstrumentor

langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
    CrewAIInstrumentor().instrument(skip_dep_check=True)
    LiteLLMInstrumentor().instrument()
else:
    print("Authentication failed. Please check your credentials and host.")
