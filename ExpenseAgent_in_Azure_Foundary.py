from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
from dotenv import load_dotenv
import os
import time
import re
from pathlib import Path

load_dotenv()

# Initialize the AI Project
project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=os.environ.get('PROJECT_ENDPOINT')
)

# Get the agent
agent = project.agents.get_agent(os.environ.get('EXPENSE_AGENT_ID'))

# Create a new conversation thread
thread = project.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Initial user message
message = project.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="I'd like to submit a claim for a meal."
)

# Main loop to interact with the agent until task is done
while True:
    run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

  # Wait until the run completes
    while run.status not in ["completed", "failed", "cancelled"]:
        time.sleep(1)
        run = project.agents.runs.get(thread_id=thread.id, run_id=run.id)

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
        break

    elif run.status == "cancelled":
        print("Run was cancelled.")
        break

    # Get all messages in thread, newest last
    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)

    # Display agent messages
    last_agent_message = None

    for message in messages:
        if message.role == "assistant" and message.text_messages:
            last_agent_message = message.text_messages[-1].text.value
            print(f"Agent: {last_agent_message}")

    # Check if agent is asking for more input
    if "please provide" in last_agent_message.lower() or "could you" in last_agent_message.lower():
        user_input = input("Your response: ")
        project.agents.messages.create(thread_id=thread.id, role="user", content=user_input)
    else:
        # No further input requested — assume job is done
        print("Agent task is complete.")

        # Extract sandbox link(s)
        sandbox_links = re.findall(r"\[.*?\]\((sandbox:.+?)\)", last_agent_message)

        if sandbox_links:
            # Retrieve all messages including file annotations
            messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)

            for msg in messages:
                if msg.file_path_annotations:
                    for ann in msg.file_path_annotations:
                        file_id = ann.file_path.file_id
                        file_name = f"{file_id}.txt"
                        save_path = Path.cwd() / file_name

                        project.agents.files.save(file_id=file_id, file_name=str(save_path))
                        print(f"Downloaded file to: {save_path}")
        else:
            print("No downloadable file link detected.")
        break


 