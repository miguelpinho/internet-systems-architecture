from flask import request, g
from ApiUtils.db import get_db
from DbInterface import bots
from ApiControllers.Auth import auth_verification
from ApiControllers.exceptions import *
from Utils.consts import AuthType
from ApiUtils.msg_queue import get_queue_channel, get_queue_connection, publish_bot_message


def decorate_bot_routes(flask_app: Flask):
    @flask_app.route("/api/bot", methods=['POST'])
    @auth_verification(AuthType.AUTH_TYPE_BOT)
    def bot():
        # Receives Token and Message in POST body
        try:
            content = request.json
            message = content["message"]
            bot_building = g.auth_params["bot_building"]

            connection = get_queue_connection()
            channel = get_queue_channel(connection)
            publish_bot_message(channel, bot_building, message)
            channel.close()
            connection.close()
        except (IndexError, TypeError):
            raise InvalidRequest("token and/or message not valid")

        return jsonify({"Message": message, "Building": bot_building, "Result": "Message Sent"}), 200
