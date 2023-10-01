import json

from flask_restful import Resource 
from flask import jsonify, request, make_response
from app.utils.common import push_to_async
from app.views.events.helper import send_welcome_note_to_employee
from app.views.events.helper import invite_user_to_channel
from app.views.events.helper import respond_to_message
from app.constants import SLACK_WORKSPACE_ID
from app.constants import GENERAL_ANNOUCEMENT_SLACK_CHANNEL
from app.constants import BOT_SLACK_USER_ID
from app.utils.common import get_logger

logger = get_logger()

class EventsView(Resource):
    def post(self):
        content = request.json
        if content.get('challenge'):
            return jsonify({"challenge":content['challenge']})
        #loggger.info(f"\nSlack Headers {request.headers}")
        logger.info(f"\nSlack Events payload: {content}")

        event = content.get("event",{})
        event_type = content.get("event",{}).get("type")
        channel_id = content.get("event",{}).get("channel")
        team_id = content.get("team_id",{})
        user = content.get("event",{}).get("user")
        text = content.get("event",{}).get("text","")
        # user id sent in events payload but in few events its sent as nested object under user
        
        # when new member joins slack workspave then invite user automatically to few pre-defined channels
        if event_type=='team_join' and team_id==SLACK_WORKSPACE_ID:
            user_id = user.get('id')  
            push_to_async(invite_user_to_channel, {"user_id":user_id})
        
        # when a member joins a specific team channel send a welcome note direct message
        elif event_type=='member_joined_channel' and channel_id==GENERAL_ANNOUCEMENT_SLACK_CHANNEL:
            user_id = user
            push_to_async(send_welcome_note_to_employee, {"user_id":user_id})
        
        # respond with a message when someone mentions botname
        elif event_type=="app_mention":
            push_to_async(respond_to_message, content)
        
        # ignore responding to bot replies and bot mention in the channel which might
        # create a infinite loop, hence filtering here by checking message is not from a bot user id
        if event_type=="message" and not event.get('subtype') and user and user!=BOT_SLACK_USER_ID and BOT_SLACK_USER_ID not in text:
            push_to_async(respond_to_message, content)
        
        return make_response(jsonify({"status":"ok"}), 200)

