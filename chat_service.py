import json
import openai

def get_gpt_response(messages):
    with open("credentials/openai_api_key.json", "r") as f:
        openai_config = json.load(f)
        
    openai.api_key = openai_config["api_key"]
    
    system_prompt = """
    you are chatbot and you are talking to a human.
    you answer politely and try to help the human.
    response sentences consist by 5 ~ 20 words.
    """
    messages[0]["content"] = system_prompt

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    if response and response['choices']:
        return response['choices'][0]['message']['content']

    return "Sorry, I couldn't generate a response."
