import random
import json
import os

from app.services.slack.helper import send_slack_message
from app.services.slack.helper import get_channel_id_for_user
from app.services.slack.helper import open_model_in_slack
from app.services.openai.helper import get_text_from_openai
from app.services.gcp.helper import push_data_to_sheets
from app.constants import GENERAL_ANNOUCEMENT_SLACK_CHANNEL
from app.constants import HR_SLACK_USER_ID
from app.constants import SPREADSHEET_ID
from app.utils.common import get_logger

logger = get_logger()

def handle_form_submission(**payload):
    logger.info("\n\n1. Sending a new employee introduction message to team channel...")
    post_a_slack_message_to_team_channel(payload)

    logger.info("\n\n2. Sending onboarding success message to employee")
    send_onboarding_success_message_to_employee(payload['user_id'])

    logger.info("\n\n3. Sending onboarding details to HR")
    send_onboarding_complete_dm_to_HR(payload)

def generate_onboarding_introduction_text(payload):
    temperature=[0.8,1,0.8,0.8,0.8,1.2,1.2,0.8]
    dynamic_temp=random.choice(temperature)
    data = {
        "model": "gpt-3.5-turbo",
        "temperature":dynamic_temp,
        "max_tokens": 3000,
        "messages": [
            {
            "role": "system",
            "content": "You are a helpful assistant."
            },
            {
            "role": "system",
            "content": f"Create a detailed long intro with few emojis in third party tone for a new employee on behalf of Signeasy where Employee Name is\
                {payload['name']}, Employee hometown is {payload['location']}, Experience is {payload['exp']} years in {payload['team']}, \
                Prevoius projects are  {payload['team']}, birthday is {payload['dob']} and hobby is {payload['hobby']}. \
                Employee email is {payload['email']}.Previous org {payload['prev_org']}. Mention all details collected. Ask to reach Loina & Sravan from HR team for help via chat. Regards HR team"
            }
        ]
    }

    content = get_text_from_openai(data)
    return content

def post_a_slack_message_to_team_channel(payload):
    content = generate_onboarding_introduction_text(payload)
    payload = {
        "channel": f"{GENERAL_ANNOUCEMENT_SLACK_CHANNEL}",
        "user": f"{payload['user_id']}",
        "blocks":  [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "@channel"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🚨 Introducing Our Newest Team Member: <@{payload['user_id']}> 🎉"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{content}"
                }
            },
            {
                "type": "divider"
            }
        ]
    }
    send_slack_message(payload)

def send_onboarding_success_message_to_employee(user_id):
    temperature=[0.8,1,0.8,0.8,0.8,1.2,1.2,0.8]
    dynamic_temp=random.choice(temperature)
    logger.info(dynamic_temp)
    data = {
        "model": "gpt-3.5-turbo",
        "temperature": dynamic_temp,
        "max_tokens": 60,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "system",
                "content": "create a casual short unique thankyou chat message on completing the digital onboarding. Ignore incomplete sentence do not mention greeting to employee "
            }
        ]
    }
    content = get_text_from_openai(data)
    channel_id=get_channel_id_for_user(user_id)
    payload={
        "channel": f"{channel_id}",
        "user": f"{user_id}",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hi <@{user_id}> :wave:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{content}"
                }
            },
            {
                "type": "image",
                "image_url": "https://media.giphy.com/media/fXstWMEGHv9wXkOmNr/giphy.gif",
                "alt_text": "inspiration"
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Before you dive in, take a quick peek at some must-reads:",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "1️⃣ <https://coda.io/docs|*Employee Handbook* >- Our Company cheat sheet. \n 2️⃣ <https://coda.io/docs|*Code of Conduct* > - How we roll together.\n:three:<https://coda.io/docs|* Company wiki* > - Detailed information about organizational structure."
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "🎉Also, your intro message is out in the wild. Checkout #general-annoucement"
                }
            }
        ]
    }
    send_slack_message(payload)

def send_onboarding_complete_dm_to_HR(onboarding_details):
    # generate text using prompts passed to chatgpt
    temperature=[0.8,1,0.8,0.8,0.8,1.2,1.2,0.8]
    dynamic_temp=random.choice(temperature)
    logger.info(dynamic_temp)
    data = {
        "model": "gpt-3.5-turbo",
        "temperature": dynamic_temp,
        "max_tokens": 60,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "system",
                "content": f"create a short casual FYI chat message for HR manager informing employee named {onboarding_details['name']} completed the onboarding. Ignore incomplete sentences at end. Don't mention greetings at the start. Do not mention Hi, Hello, Hey at the start"
            }
        ]
    }
    content = get_text_from_openai(data)
    content = content.replace(onboarding_details['name'], f"<@{onboarding_details['user_id']}>")

    #update google sheets
    push_data_to_sheets(onboarding_details)

    #send slack message to HR
    channel_id=get_channel_id_for_user(HR_SLACK_USER_ID)
    payload={
        "channel": f"{channel_id}",
            "user": f"{HR_SLACK_USER_ID}",
            "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hi <@{HR_SLACK_USER_ID}> :wave:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{content}"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View Onboarding Details",
                        "emoji": True
                    },
                    "value": "Check details",
                    "url": f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=0",
                    "action_id": "button-action"
                }
            }
        ]
    }
    send_slack_message(payload)

def open_onboarding_form(trigger_id):
    curr_dir = os.getcwd()
    f = open(curr_dir + '/app/data/modal_payloads/onboarding_modal_v1.json')
    # returns JSON object as a dictionary
    data = json.load(f)
    data = json.dumps(data).replace("{trigger}", trigger_id)
    data = json.loads(data)
    open_model_in_slack(data)
    f.close()

    