# -*- coding: utf-8 -*-

from app.constants import HTTP_HOST
from app.constants import HTTP_PORT
from app.constants import *
from flask import Flask
from flask_restful import Api

from app.views.events.event import EventsView
from app.views.interactions.interaction import InteractionsView

app = Flask(__name__)
api = Api(app)

api.add_resource(EventsView, '/v1/events')
api.add_resource(InteractionsView, '/v1/interact')

if __name__ == "__main__":
    app.run(debug=True, host=HTTP_HOST, port=HTTP_PORT)
