from flask import Flask, request, jsonify, g

from ApiControllers.auth import auth_verification
from ApiControllers.exceptions import InvalidRequest
from ApiUtils.db import get_db
from ApiControllers.auth.exceptions import NotAuthenticated
from DbInterface import user


def decorate_user_routes(flask_app: Flask):
    """ Decorates The Routes related with the user api (/api/user/)"""

    @flask_app.route("/api/user/messages", methods=["GET", "POST"])
    @auth_verification()  # This is the middleware for authentication
    def user_messages():
        """ Handles User Messages - Inserts messages or gets them, based on the http method (POST, GET) """
        # Receives uuid on the user from the middleware (not yet implemented, currently receives a "Fake UUID")
        if 'auth_params' in g:
            user_params = g.auth_params
            user_id = user_params["uuid"]
        else:
            # Something wrong could have happen with the middleware, so throw unauthorized error
            raise NotAuthenticated("Please Authenticate First")

        if request.method == "POST":  # Handle new message creation
            try:
                message = request.json["message"]
                user.send_msg(get_db(), user_params["uuid"], message)
            except (IndexError, TypeError):
                raise InvalidRequest("message not valid")

            # Handle the request properly
            return jsonify({"UserId": user_id, "Message": message, "Result": "Message Sent"}), 200

        else:  # Handle the request for a list of messages (GET)
            try:
                message_list = user.get_msgs(get_db(), user_id)

            except Exception:  # TODO: Change this with a explicit exception
                raise InvalidRequest("message not valid")  # TODO: Set a meaningful Exception and Message

            return jsonify({"UserId": user_id, "Messages": message_list})

    @flask_app.route("/api/user/location", methods=["POST"])
    @auth_verification()  # This is the middleware for authentication
    def user_location():
        """ Handles User Location - Inserts user location"""
        # Receives uuid on the user from the middleware (not yet implemented, currently receives a "Fake UUID")
        if 'auth_params' in g:
            user_params = g.auth_params
            user_id = user_params["uuid"]
        else:
            # Something wrong could have happen with the middleware, so throw unauthorized error
            raise NotAuthenticated("Please Authenticate First")

        try:
            content = request.json
            latitude = content["lat"]
            longitude = content["lon"]
            user.set_position(get_db(), user_id, latitude, longitude)

        except (TypeError, IndexError) as e:
            raise InvalidRequest("Latitude or Longitude not valid: " + str(e))

        except Exception:  # TODO: Change this with a explicit exception that reflects exceptions generated from
            # user.set_position()
            raise InvalidRequest("message not valid")

        return jsonify({"UserId": user_id, "Result": "Location Set", "Latitude": latitude, "Longitude": longitude}), 200

    @flask_app.route("/api/user/building", methods=["GET"])
    @auth_verification()  # This is the middleware for authentication
    def user_building():
        """ Handles User Building - Gets user location"""
        if 'auth_params' in g:
            user_params = g.auth_params
            user_id = user_params["uuid"]
        else:
            # Something wrong could have happen with the middleware, so throw unauthorized error
            raise NotAuthenticated("Please Authenticate First")
        try:
            building = user.get_user_building(get_db(), user_id)

            if building is None:
                raise InvalidRequest("User isn't in a building")
            else:
                return jsonify({"UserId": user_id, "Building": building}), 200

        except Exception:# TODO: Change this with a explicit exception that reflects exceptions generated from
            # user.get_user_building()
            raise InvalidRequest("User isn't in a building")

    @flask_app.route("/api/user/radius", methods=["POST"])
    @auth_verification()  # This is the middleware for authentication
    def user_radius():
        """ Handles User message radius - Sets user message radius"""

        return jsonify({"UserId": "This will have some user", "Radius": "5"}), 200

    @flask_app.route("/api/user/nearby", methods=["GET"])
    @auth_verification()  # This is the middleware for authentication
    def user_nearby():
        """ Handles User nearby users - Gets nearby users"""

        return jsonify({"UserId": "This will have some user", "users": ["user1", "user2", "user3"]}), 200
