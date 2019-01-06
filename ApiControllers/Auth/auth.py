from flask import Flask, request, jsonify, url_for, render_template, Response, json, current_app, redirect
import fenixedu
from ApiControllers import exceptions
import uuid
from Utils.consts import Tokens, FenixApi


def decorate_auth_handlers(flask_app: Flask):
    @flask_app.route("/auth/login", methods=["GET", "POST"])
    def auth_login():
        if request.method == "GET":
            # Receives Code from fenix api in the args, uses it to get user info
            code = request.args.get("code")
            # Get info from Fenix API
            config = fenixedu.FenixEduConfiguration(current_app.private_consts.FenixApi.FENIX_API_CLIENT_ID,
                                                    url_for("auth_login", _external=True),
                                                    current_app.private_consts.FenixApi.FENIX_API_CLIENT_SECRET)
            # Get the access token from the response, we choose not to do refreshes - just one time access to get info
            client = fenixedu.FenixEduClient(config)
            user = client.get_user_by_code(code)
            try:
                person = client.get_person(user)
                person_name = person["name"]
                person_id = person["username"]
                print(f"Name: {person_name}, id:{person_id}")
                # TODO: Assert for the user in the database
            except TypeError as e:
                raise exceptions.InvalidRequest("Invalid login request, please try again: " + str(e))
        else:
            # Receives password and admin name in the POST body
            # compares it to the credentials
            pass

        # Create new token (Unique) - This only occurs in succesful logins
        token = uuid.uuid4()
        # TODO: Add token to cache - with the user name and id set in. Use token as cache key for faster access in
        # each token comparisson

        if request.method == "GET":  # Handle web client with redirection and token feeding
            redir = redirect(url_for("dashboard", _external=True))
            redir.set_cookie("x-auth", token.bytes)  # Give the user a cookie, eases with following requests
            return redir

        # For the admin give only a header, as it is a REST client
        resp = jsonify({"message": "login succesful"})
        resp.headers["x-auth"] = token
        return resp

    @flask_app.route("/auth/client_id")
    def auth_client_id():
        client_id = current_app.private_consts.FenixApi.FENIX_API_CLIENT_ID
        redirect_url = url_for("auth_login", _external=True)

        return jsonify({"client_id": client_id, "redirect_url": redirect_url})
