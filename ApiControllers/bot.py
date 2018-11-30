from flask import request, g
from ApiUtils.db import get_db
from DbInterface import bots
from ApiControllers.auth import auth_verification
from ApiControllers.exceptions import *
from Utils.consts import AuthType


def decorate_bot_routes(flask_app: Flask):
    @flask_app.route("/api/bot", methods=['POST'])
    @auth_verification(AuthType.AUTH_TYPE_BOT)
    def bot():
        # Receives Token and Message in POST body
        try:
            content = request.json
            message = content["message"]
            # g.pop("db") gets the session db object
            # g.pop("uuid") gets the bot_token
            # If there is some problem with the request in the bot.send_msg() throw an exception
            bots.send_msg(get_db(), g.uuid, message)
        except (IndexError, TypeError):
            raise InvalidRequest("token and/or message not valid")

        # Handle the request properly

        return jsonify({"Message": message, "Result": "Message Sent"}), 200
