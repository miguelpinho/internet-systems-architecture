from flask import request

from ApiControllers.exceptions import *


def decorate_bot_routes(flask_app: Flask):
    @flask_app.route("/api/bot", methods=['POST'])
    def bot():
        # Receives Token and Message in POST body
        try:
            content = request.json
            message = content["message"]
            token = content["token"]
        except (IndexError, TypeError):
            raise InvalidRequest("token and/or message not valid")

        # Handle the request properly

        return jsonify({"Token": token,  "Message": message, "Result": "Message Sent"}), 200
