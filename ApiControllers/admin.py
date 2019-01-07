from flask import Flask, request, jsonify, current_app

from ApiControllers.Auth.middleware import auth_verification
from Utils.consts import AuthType
from .ApiUtils.db import get_db
from DbInterface import bots, buildings, logs
from .exceptions import InvalidRequest


def decorate_admin_routes(flask_app: Flask):
    decorate_admin_bots(flask_app)
    decorate_admin_buildings(flask_app)
    decorate_admin_logs(flask_app)


def decorate_admin_bots(flask_app: Flask):
    @flask_app.route("/api/admin/bots", methods=["POST", "GET"])
    @auth_verification(AuthType.AUTH_TYPE_ADMIN)
    def admin_bots():
        try:
            response = {}
            if request.method == "GET":
                # List of all the bots
                bots_list = bots.list_bots(get_db())
                status = 200
                response["bots"] = bots_list
            else:
                # Creates new bot, building is passed in the body
                bot_token = bots.add_bot(get_db(), request.json["building"], cache=current_app.cache)
                status = 200
                response["token"] = bot_token

            return jsonify(response), status

        except IndexError as e:
            return InvalidRequest("Could not fulfill the request " + str(e))

    @flask_app.route("/api/admin/bots/<token>", methods=["GET", "DELETE"])
    @auth_verification(AuthType.AUTH_TYPE_ADMIN)
    def admin_bots_id(token=None):
        try:
            response = {}
            status = 200
            if request.method == "GET":
                # Return the bot building, and maybe other info
                building = bots.where_is_bot(get_db(), token, cache=current_app.cache)
                status = 200
                response["building"] = building
            else:
                # Deletes a bot, bot id (token) is passed in query
                deleted_bot = bots.delete_bot(get_db(), token, cache=current_app.cache)
                status = 200
                response["bot_info"] = deleted_bot
            return response, status

        except IndexError as e:
            return InvalidRequest("Could not fulfill the request " + str(e))


def decorate_admin_buildings(flask_app: Flask):
    @flask_app.route("/api/admin/buildings", methods=["POST", "GET"])
    @auth_verification(AuthType.AUTH_TYPE_ADMIN)
    def admin_buildings():
        try:
            response = {}
            if request.method == "GET":
                # List of all the buildings (name and id)
                buildings_list = buildings.show_all_buildings(get_db())
                status = 200
                response["buildings"] = buildings_list
            else:
                # Creates new building, info is passed on the body
                body = request.json
                bid = body["id"]
                bname = body["name"]
                lat = body["latitude"]
                lon = body["longitude"]
                rad = body["radius"]
                new_building = buildings.add_building(get_db(), bid, bname, lat, lon, rad)
                status = 200
                response["building"] = new_building

            return jsonify(response), status

        except IndexError as e:
            return InvalidRequest("Could not fulfill the request " + str(e))

    @flask_app.route("/api/admin/bots/<bid>", methods=["GET", "DELETE"])
    @auth_verification(AuthType.AUTH_TYPE_ADMIN)
    def admin_buildings_id(bid=None):
        try:
            response = {}
            if request.method == "GET":
                # Return the building info, users list and bots list
                building = buildings.show_info(get_db(), bid)
                status = 200
                response["building"] = building
            else:
                # Deletes a building, building id (bid) is passed in query
                body = request.json
                bid = body["id"]
                deleted_bot = bots.delete_bot(get_db(), bid)
                status = 200
                response["bot_info"] = deleted_bot

            return jsonify(response), status

        except IndexError as e:
            return InvalidRequest("Could not fulfill the request " + str(e))


def decorate_admin_logs(flask_app: Flask):
    @flask_app.route("/api/admin/logs/users/<ist_id>/messages", methods=["GET"])
    @auth_verification(AuthType.AUTH_TYPE_ADMIN)
    def admin_logs_messages(ist_id=None):
        # Returns messages for that user
        try:
            response = {}
            message_log = logs.get_msgs_user(get_db(), ist_id)
            status = 200
            response["logs"] = message_log
            return jsonify(response), status
        except IndexError as e:
            return InvalidRequest("Could not fulfill the request " + str(e))

    @flask_app.route("/api/admin/logs/users/<ist_id>/moves", methods=["GET"])
    @auth_verification(AuthType.AUTH_TYPE_ADMIN)
    def admin_logs_moves(ist_id=None):
        # Returns moves for that user
        try:
            response = {}
            moves_log = logs.get_moves(get_db(), ist_id)
            status = 200
            response["logs"] = moves_log
            return jsonify(response), status
        except IndexError as e:
            return InvalidRequest("Could not fulfill the request " + str(e))

    @flask_app.route("/api/admin/logs/building/<bid>", methods=["GET"])
    @auth_verification(AuthType.AUTH_TYPE_ADMIN)
    def admin_logs_building(bid=None):
        # Returns messages in that building
        try:
            response = {}
            building_log = logs.get_msgs_building(get_db(), bid)
            status = 200
            response["logs"] = building_log
            return jsonify(response), status
        except IndexError as e:
            return InvalidRequest("Could not fulfill the request " + str(e))
