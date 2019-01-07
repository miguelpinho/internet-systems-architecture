from time import strftime, gmtime

from flask import Flask, request, jsonify, g, current_app, json

from ApiControllers.Auth import auth_verification
from ApiControllers.exceptions import InvalidRequest
from ApiUtils.db import get_db
from ApiControllers.Auth.exceptions import NotAuthenticated
from DbInterface.user import get_position
from msg_queue import get_queue_connection, get_queue_channel, publish_user_message


def decorate_user_routes(flask_app: Flask):
    """ Decorates The Routes related with the user api (/api/user/)"""

    @flask_app.route("/api/user/messages", methods=["POST"])
    @auth_verification()  # This is the middleware for authentication
    def user_messages():
        """ Handles User Messages - Send messages to the message queues"""
        # Receives uuid on the user from the middleware (not yet implemented, currently receives a "Fake UUID")
        if 'auth_params' in g:
            user_params = g.auth_params
            user_id = user_params["user_id"]

        if request.method == "POST":  # Handle new message creation
            try:
                message = request.json["message"]
                content = {"message": message, "user_id": user_id}
                radius = request.json["radius"]
                queue_message = json.dumps({"radius": radius, "content": content})
                connection = get_queue_connection()
                channel = get_queue_channel(connection)
                publish_user_message(channel, queue_message)
                channel.close()
                connection.close()
            except (IndexError, TypeError) as e:
                raise InvalidRequest("message not valid", str(e))

            # Handle the request properly
            return jsonify({"UserId": user_id, "Message": {"text": message, "time": strftime("%Y-%m-%d %H:%M:%S",
                            gmtime()), "from": user_id}, "Result": "Message Sent"}), 200

    @flask_app.route("/api/user/building", methods=["GET"])
    @auth_verification()  # This is the middleware for authentication
    def user_building():
        """ Handles User Building - Gets user location"""
        if 'auth_params' in g:
            user_params = g.auth_params
            user_id = user_params["user_id"]
        else:
            # Something wrong could have happen with the middleware, so throw unauthorized error
            raise NotAuthenticated("Please Authenticate First")
        try:
            building = user.get_user_building(get_db(), user_id)
            if building is None:
                building = "Outside"
            return jsonify({"UserId": user_id, "Building": building}), 200
        except TypeError as e:
            raise InvalidRequest("Cannot fetch user building correctly: " + str(e))

    @flask_app.route("/api/user/nearby", methods=["GET"])
    @auth_verification()  # This is the middleware for authentication
    def user_nearby():
        """ Handles User nearby users - Gets nearby users"""
        if 'auth_params' in g:
            user_params = g.auth_params
            user_id = user_params["user_id"]
        else:
            # Something wrong could have happen with the middleware, so throw unauthorized error
            raise NotAuthenticated("Please Authenticate First")
        try:
            content = request.args
            radius = content.get("radius")
            users_list = user.get_close_users(get_db(), user_id, float(radius))
            if users_list is None:
                # return msg "No users close by"
                pass
            else:
                return jsonify({"UserId": user_id, "users": users_list}), 200

        except Exception as e:
            raise InvalidRequest("Error in getting nearby users:", str(e))

