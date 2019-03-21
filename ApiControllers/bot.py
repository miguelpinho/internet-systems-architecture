from flask import request, g
from ApiControllers.Auth import auth_verification
from ApiControllers.exceptions import *
from .ApiUtils.msg_queue import get_queue_channel, get_queue_connection, publish_bot_message
from Utils.consts import AuthType
from DbInterface.buildings import show_info
from ApiControllers.ApiUtils.db import get_db
import json as json_engine


def decorate_bot_routes(flask_app: Flask):
    @flask_app.route("/api/bot", methods=['POST'])
    @auth_verification(AuthType.AUTH_TYPE_BOT)
    def bot():
        # Receives Token and Message in POST body
        try:
            db = get_db()
            content = request.json
            bot_token = g.auth_params["bot_id"]
            bot_building_id = g.auth_params["bot_building"]
            message = json_engine.dumps({"text": content["message"], "building": bot_building_id})

            connection = get_queue_connection()
            channel = get_queue_channel(connection)
            # By publishing with bot_building as routing-key, the message is filtered to the correct subscribers
            publish_bot_message(channel, str(bot_building_id), message)
            channel.close()
            connection.close()
        except (IndexError, TypeError) as e :
            raise InvalidRequest("token and/or message not valid")

        return jsonify({"Message": message, "Building": bot_building_id, "Result": "Message Sent"}), 200
