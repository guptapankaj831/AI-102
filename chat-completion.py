from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.inference.models import SystemMessage, UserMessage
from openai import AzureOpenAI
import os

# Chat completion using AzureOpenAI with model url and subscription_key
try:
    ## Get a chat client
    url = os.environ.get('MODEL_URL')
    deployment = os.environ.get('MODEL_NAME')
    subscription_key = os.environ.get('SUBSCRIPTION_KEY')

    chat_client = AzureOpenAI(
            azure_endpoint=url,
            api_key=subscription_key,
            api_version=os.environ.get('API_VERSION'))

    # Get a chat completion based on a user-provided prompt
    user_prompt = input("Enter Text: ")

    response = chat_client.chat.completions.create(
        model=deployment,
        messages=[
            SystemMessage("You are a helpful AI assistant that answers questions."),
            UserMessage(user_prompt)
        ],
    )
    print(response.choices[0].message.content)

except Exception as ex:
    print(ex)


# Chat completion using AIProjectClient with project endpoint url and System Identity Credential
try:
    ## Get a chat client
    chat_client = AIProjectClient(            
        credential=DefaultAzureCredential(),
        endpoint=os.environ.get('PROJECT_ENDPOINT'))

    ## Get an Azure OpenAI chat client
    openai_client = chat_client.inference.get_azure_openai_client(api_version=os.environ.get('API_VERSION'))

    # Get a chat completion based on a user-provided prompt
    user_prompt = 'What is capital of india' # input("Enter Text: ")

    response = openai_client.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
            SystemMessage("You are a helpful AI assistant that answers questions."),
            UserMessage(user_prompt)
        ],
    )
    print(response.choices[0].message.content)

except Exception as ex:
    print(ex)
