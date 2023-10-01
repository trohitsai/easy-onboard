import json

from flask_restful import Resource 
from flask import  jsonify, request
from app.utils.common import push_to_async
from app.views.interactions.helper import open_onboarding_form
from app.views.interactions.helper import handle_form_submission
from app.utils.common import get_logger

logger = get_logger()

class InteractionsView(Resource):
    def post(self):
        content = request.form
        logger.info(f"Interaction payload - > {content}")
        payload = json.loads(dict(request.form).get("payload"))
        if payload.get("type")=='view_submission':
            data=self.get_input_from_modal_submitted(payload)
            push_to_async(
                handle_form_submission,{
                    "name": data["name"],
                    "location": data["location"],
                    "exp": data['exp'],
                    "dob": data['dob'],
                    "hobby": data['hobby'],
                    "user_id": data['user_id'],
                    "team": data["team"],
                    "email": data["email"],
                    "prev_org":data["prev_org"],
                    "dept":data["dept"]
                } 
            )
            return {}, 200  
            # this closes the model. we have respond success status in 3secs
                
        elif payload.get("type")=='block_actions':
            if payload.get("actions")[0]["value"]=="onboard_me_button":
                trigger_id=payload["trigger_id"]
                open_onboarding_form(trigger_id)
            
        return {}, 200
    
    def get_input_from_modal_submitted(self, payload):
        employee_name_bid=None
        email_bid=None
        dob_bid=None
        location_bid=None
        teamjoined_bid=None
        exp_bid=None
        prev_org_bid=None
        hobby_bid=None
        dep_bid=None

        for block in payload["view"]["blocks"]:
            if block["label"]["text"]=="Name":
                employee_name_bid= block["block_id"]
            elif block["label"]["text"]=="Email":
                email_bid= block["block_id"]
            elif block["label"]["text"]=="Date of birth":
                dob_bid= block["block_id"]
            elif block["label"]["text"]=="Hometown":
                location_bid= block["block_id"]
            elif block["label"]["text"]=="Team joined":
                teamjoined_bid= block["block_id"]
            elif block["label"]["text"]=="Experience":
                exp_bid= block["block_id"]
            elif block["label"]["text"]=="Previous Organisation":
                prev_org_bid= block["block_id"]
            elif block["label"]["text"]=="Hobbies":
                hobby_bid= block["block_id"]
            elif block["label"]["text"]=="Department":
                dep_bid= block["block_id"]
        
        values = payload["view"]["state"]["values"]
        text_input="plain_text_input-action"

        return {
            "name": values[employee_name_bid][text_input]["value"],
            "email": values[email_bid]["email_text_input-action"]["value"],
            "dob": values[dob_bid]["datepicker-action"]["selected_date"],
            "location":values[location_bid][text_input]["value"],
            "team":values[teamjoined_bid][text_input]["value"],
            "exp":values[exp_bid]["number_input-action"]["value"],
            "prev_org":values[prev_org_bid][text_input]["value"],
            "hobby":values[hobby_bid][text_input]["value"],
            "user_id":payload["user"]["id"],
            "dept":values[dep_bid]["static_select-action"]["selected_option"]["text"]["text"]
        }