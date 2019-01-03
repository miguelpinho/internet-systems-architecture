from time import strftime, gmtime

from flask import Flask, request, jsonify, g

from ApiControllers.Auth import auth_verification
from ApiControllers.exceptions import InvalidRequest
from ApiUtils.db import get_db
from ApiControllers.Auth.exceptions import NotAuthenticated
from DbInterface import user


def decorate_user_routes(flask_app: Flask, private_consts):
    """ Decorates The Routes related with the user api (/api/user/)"""

    @flask_app.route("/api/user/messages", methods=["POST"])
    @auth_verification()  # This is the middleware for authentication
    def user_messages():
        """ Handles User Messages - Send messages to the message queues"""
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
                content = {"message": message, "user_id": user_id}
                radius = request.json["radius"]
                #  queue.send_user_msg(content, radius)
            except (IndexError, TypeError):
                raise InvalidRequest("message not valid")

            # Handle the request properly
            return jsonify({"UserId": user_id, "Message": {"text": message, "time": strftime("%Y-%m-%d %H:%M:%S",
                            gmtime()), "from": user_id}, "Result": "Message Sent"}), 200


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
            user.set_position(get_db(private_consts), user_id, latitude, longitude)

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
            building = user.get_user_building(get_db(private_consts), user_id)
            return jsonify({"UserId": user_id, "Building": building}), 200
        except TypeError as e:
            raise InvalidRequest("Cannot fetch user building correctly: " + str(e))
        except Exception:# TODO: Change this with a explicit exception that reflects exceptions generated from
            # user.get_user_building()
            raise InvalidRequest("User isn't in a building")

    @flask_app.route("/api/user/radius", methods=["POST"])
    @auth_verification()  # This is the middleware for authentication
    def user_radius():
        """ Handles User message radius - Sets user message radius"""
        if 'auth_params' in g:
            user_params = g.auth_params
            user_id = user_params["uuid"]
        else:
            # Something wrong could have happen with the middleware, so throw unauthorized error
            raise NotAuthenticated("Please Authenticate First")
        try:
            content = request.json
            radius = content["radius"]
            #user.set_radius(get_db(private_consts), user_id, radius)
            return jsonify({"UserId": user_id, "Radius": radius}), 200

        except (TypeError, IndexError) as e:
            raise InvalidRequest("Radius not valid: " + str(e))

        except Exception:  # TODO: Change this with a explicit exception that reflects exceptions generated from
            # user.get_user_building()
            raise InvalidRequest("User isn't in a building")


    @flask_app.route("/api/user/nearby", methods=["GET"])
    @auth_verification()  # This is the middleware for authentication
    def user_nearby():
        """ Handles User nearby users - Gets nearby users"""
        if 'auth_params' in g:
            user_params = g.auth_params
            user_id = user_params["uuid"]
        else:
            # Something wrong could have happen with the middleware, so throw unauthorized error
            raise NotAuthenticated("Please Authenticate First")
        try:
            content = request.json
            radius = content["radius"]
            users_list = user.get_close_users(get_db(private_consts), user_id, radius)
            if users_list is None:
                # return msg "No users close by"
                pass
            else:
                return jsonify({"UserId": user_id, "users": users_list}), 200

        except Exception:  # TODO: Change this with a explicit exception that reflects exceptions generated from
            # user.get_close_users()
            raise InvalidRequest("Some error")

