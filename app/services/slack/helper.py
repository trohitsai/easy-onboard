import requests
import json
from app.constants import SLACK_BOT_TOKEN
from app.utils.common import get_logger

logger = get_logger()

def send_slack_message(payload):
    url = "https://slack.com/api/chat.postMessage"

    payload = json.dumps(payload)
    headers = {
        'Authorization': SLACK_BOT_TOKEN,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code!=200:
        logger.error(response.json())
    logger.info(response.json())

# needed to post a slack dm message to a user
def get_channel_id_for_user(user_id):
    url = "https://slack.com/api/conversations.open"

    payload = json.dumps({
        "users": f"{user_id}",
        "prevent_creation": True,
        "return_im": True
    })

    headers = {
        'Authorization': SLACK_BOT_TOKEN,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code!=200:
        logger.error(response.json())
        return None
    channel_id=(response.json()).get("channel")["id"]
    return channel_id

def open_model_in_slack(payload):
    url = "https://slack.com/api/views.open"
    # evrything required is in paylaod itself
    payload=json.dumps(payload)

    headers = {
        'Authorization': SLACK_BOT_TOKEN,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if (response.json()).get("ok")==False:
        logger.error(response.json())