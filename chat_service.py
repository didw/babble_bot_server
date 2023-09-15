import json
import openai

def get_gpt_response(messages):
    with open("credentials/openai_api_key.json", "r") as f:
        openai_config = json.load(f)
        
    openai.api_key = openai_config["api_key"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    if response and response['choices']:
        return response['choices'][0]['message']['content']

    return "Sorry, I couldn't generate a response."
