from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv

load_dotenv()

# Load all connections in the project
project_endpoint = os.environ.get('PROJECT_ENDPOINT')

try:
    # Get project client
    project_client = AIProjectClient(
            endpoint=project_endpoint,
            credential=DefaultAzureCredential()
        )

    ## List all connections in the project
    connections = project_client.connections
    print(f"List all connections: {connections}")
    for connection in connections.list():
        print(f"{connection.name} ({connection.type})")

except Exception as ex:
    print(ex)