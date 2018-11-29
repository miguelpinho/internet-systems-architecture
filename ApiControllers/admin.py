from flask import Flask, request, g

from Db.db import get_db
from DbInterface import bots
from exceptions import InvalidRequest


def decorate_admin_routes(flask_app: Flask):
    decorate_admin_bots(flask_app)
    decorate_admin_buildings(flask_app)
    decorate_admin_logs(flask_app)


def decorate_admin_bots(flask_app: Flask):
    @flask_app.route("/api/admin/bots", methods=["POST", "GET"])
    def admin_bots():
        try:
            response = {}
            if request.method == "GET":
                # List of all the bots
                bots_list = bots.list_bots(get_db())
                response.status = 200
                response.bots = bots_list
            else:
                # Creates new bot, building is passed in the body
                bot_token = bots.add_bot(get_db(), request.json["building"])
                response.status = 200
                response.bot_token = bot_token

            return response

        except IndexError:
            return InvalidRequest("Could not fulfill the request")

    @flask_app.route("/api/admin/bots/<token>", methods=["GET", "DELETE"])
    def admin_bots_id(token=None):
        if request.method == "GET":
            pass
            # Return the bot building, and maybe other info

        else:
            pass
            # Deletes a bot, bot id (token) is passed in query

        return f"/api/admin/bots/${token}"


def decorate_admin_buildings(flask_app: Flask):
    @flask_app.route("/api/admin/buildings", methods=["POST", "GET"])
    def admin_buildings():
        if request.method == "GET":
            pass
            # List of all the buildings (name and id)

        else:
            pass
            # Creates new building, info is passed on the body

        return "/api/admin/buildings"

    @flask_app.route("/api/admin/bots/<bid>", methods=["GET", "DELETE"])
    def admin_buildings_id(bid=None):
        if request.method == "GET":
            pass
            # Return the building info, users list and bots list

        else:
            pass
            # Deletes a bot, building id (bid) is passed in query

        return f"/api/admin/buildings/${bid}"


def decorate_admin_logs(flask_app: Flask):
    @flask_app.route("/api/admin/logs/users/<ist_id>/messages", methods=["GET"])
    def admin_logs_messages(ist_id=None):
        # Returns messages for that user
        return f"/api/admin/logs/users/{ist_id}/messages"

    @flask_app.route("/api/admin/logs/users/<ist_id>/moves", methods=["GET"])
    def admin_logs_moves(ist_id=None):
        # Returns moves for that user
        return f"/api/admin/logs/users/{ist_id}/moves"

    @flask_app.route("/api/admin/logs/building/<bid>", methods=["GET"])
    def admin_logs_building(bid=None):
        # Returns messages in that building
        return f"/api/admin/logs/buildings/{bid}"

