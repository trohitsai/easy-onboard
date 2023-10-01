import json
import requests

from app.services.openai.helper import get_text_from_openai
from app.services.slack.helper import get_channel_id_for_user
from app.services.slack.helper import send_slack_message
from app.constants import SLACK_BOT_TOKEN
from app.constants import MADATORY_CHANNELS
from app.utils.common import get_logger

logger = get_logger()

def send_welcome_note_to_employee(**payload):
    user_id = payload['user_id']
    data = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.8,
        "max_tokens": 80,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "system",
                "content":"create a friendly short & multiline welcome chat message on joining Signeasy with few emojis.Do not keep incomplete sentences at last. Also do not mention greeting like Hey there in message. Do not mention any CTA action. do not mention to ask any questions. Request employee to complete interactive digital onboarding using below button for a quick intro.Introduce yourself as virtual onboarding bot"
            }
        ]
    }
    content = get_text_from_openai(data)
    
    channel_id = get_channel_id_for_user(user_id)
    payload = {
            "channel": f"{channel_id}",
            "user": f"{user_id}",
            "blocks":  [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hey <@{user_id}>!"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"{content}",
                    "emoji": True
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Onboard Me! 🛳️"
                        },
                        "style": "primary",
                        "value": "onboard_me_button"
                    }
                ]
            }
        ]
    }
    send_slack_message(payload)

def invite_user_to_channel(**payload):
    channels = MADATORY_CHANNELS.split(",")
    url = "https://slack.com/api/conversations.invite"

    for channel in channels:
        payload = json.dumps({
            "users": f"{payload['user_id']}",
            "channel": channel
        })
        headers = {
            'Authorization': SLACK_BOT_TOKEN,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if not (response.json())['ok'] or response.status_code!=200:
            if (response.json())['error']=="already_in_channel":
                logger.info(f"WARNING: USER ALREADY PART OF CHANNEL")
            logger.error(f"\n======>ERROR OCCURED : {response.json()}")

def respond_to_message(**payload):
    channel_id = payload['event']['channel']
    user_id = payload['event'].get('user')
    data = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.8,
        "max_tokens": 1000,
        "messages": [
            {
                "role": "system",
                "content":  "You are a helpful assistant. Your goal is to answer the following question, using the associated texts as context, as truthfully as you can."
            },
            {
                "role": "system",
                "content": f"{payload['event']['text']}"
            }
        ]
    }
    content=get_text_from_openai(data)
    payload = {
            "channel": f"{channel_id}",
            "user": f"{user_id}",
            "blocks":  [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"{content}",
                    "emoji": True
                }
            }
        ]
    }
    send_slack_message(payload)