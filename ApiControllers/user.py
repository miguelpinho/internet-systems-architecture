from flask import Flask, request, jsonify, g

from ApiControllers.auth import auth_verification
from ApiControllers.exceptions import InvalidRequest


def decorate_user_routes(flask_app: Flask):
    """ Decorates The Routes related with the user api (/api/user/)"""

    @flask_app.route("/api/user/messages", methods=["GET", "POST"])
    @auth_verification()  # This is the middleware for authentication
    def user_messages():
        """ Handles User Messages - Inserts messages or gets them, based on the http method (POST, GET) """
        # Receives uuid on the user from the middleware (not yet implemented, currently receives a "Fake UUID")
        print(g.pop("auth_params", "No auth_params passed"))

        if request.method == "POST":
            try:
                content = request.json
                message = content["message"]
            except (IndexError, TypeError):
                raise InvalidRequest("message not valid")

            # Handle the request properly
            return jsonify({"UserId": "This will have some user", "Message": message, "Result": "Message Sent"}), 200
        else:  # Handle GET request
            return jsonify({"messages": ["Message1", "Message2"]})

    @flask_app.route("/api/user/location", methods=["POST"])
    @auth_verification()  # This is the middleware for authentication
    def user_location():
        """ Handles User Location - Inserts user location"""

        return jsonify({"UserId": "This will have some user", "Result": "Location Set"}), 200

    @flask_app.route("/api/user/building", methods=["GET"])
    @auth_verification()  # This is the middleware for authentication
    def user_building():
        """ Handles User Building - Gets user location"""

        return jsonify({"UserId": "This will have some user", "Building": "Somewhere"}), 200

    @flask_app.route("/api/user/radius", methods=["POST"])
    @auth_verification()  # This is the middleware for authentication
    def user_radius():
        """ Handles User message radius - Sets user message radius"""

        return jsonify({"UserId": "This will have some user", "Radius": "5"}), 200

    @flask_app.route("/api/user/nearby", methods=["GET"])
    @auth_verification()  # This is the middleware for authentication
    def user_nearby():
        """ Handles User message radius - Sets user message radius"""

        return jsonify({"UserId": "This will have some user", "users": ["user1","user2","user3"]}), 200


