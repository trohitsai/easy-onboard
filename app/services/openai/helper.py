import requests
import json

from app.constants import OPENAI_API_KEY

def get_text_from_openai(payload):
    content=None
    url = "https://api.openai.com/v1/chat/completions"

    payload = json.dumps(payload)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': OPENAI_API_KEY
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code==200:
        content = (response.json()).get("choices")[0]["message"]["content"]

    #print(f"\nChat Gpt response: {response.json()} {response.status_code}")
    return content