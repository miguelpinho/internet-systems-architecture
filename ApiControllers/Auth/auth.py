import uuid

import fenixedu
from flask import Flask, request, jsonify, url_for, current_app, redirect

import Utils.consts as consts
import DbInterface.user as user_datastore
from ApiControllers import exceptions


def decorate_auth_handlers(flask_app: Flask):
    @flask_app.route("/auth/login", methods=["GET", "POST"])
    def auth_login():
        if request.method == "GET":  # User Login

            if not consts.USER_DEBUG:  # This debug allows to login with /auth/login?name=<some_user>

                #  Receives Code from fenix api in the args, uses it to get user info
                code = request.args.get("code")
                #  Get info from Fenix API
                config = fenixedu.FenixEduConfiguration(current_app.private_consts.FenixApi.FENIX_API_CLIENT_ID,
                                                        url_for("auth_login", _external=True),
                                                        current_app.private_consts.FenixApi.FENIX_API_CLIENT_SECRET)
                # Get the access token from the response, we choose not to do refreshes - just one time access to get
                #  info
                client = fenixedu.FenixEduClient(config)
                user = client.get_user_by_code(code)
                try:
                    person = client.get_person(user)
                    person_id = person["username"]
                except TypeError as e:
                    raise exceptions.InvalidRequest("Invalid login request, please try again: " + str(e))

            else:
                person_id = request.args.get("name")

            # Create new token (Unique) - This only occurs in succesful logins
            token = uuid.uuid4().hex
            # Add token to cache - with the user id set in. Use token as cache key for faster access in
            user_datastore.set_token(current_app.cache, token, person_id)
            # each token comparisson

            redir = redirect(url_for("dashboard", _external=True))
            redir.set_cookie("x-auth", token)  # Give the user a cookie, eases with following requests
            redir.set_cookie("username", person_id)
            return redir

        else:  # Admin Login
            # Receives password and admin name in the POST body
            body = request.json
            password = body["password"]
            username = body["username"]
            # compares it to the credentials
            if username == current_app.private_consts.AdminKeys.ADMIN_USERNAME:
                if password == current_app.private_consts.AdminKeys.ADMIN_PASSWORD:
                    # Create new token (Unique) - This only occurs in succesful logins
                    token = uuid.uuid4().hex
                    # Add token to cache - with the user id set in. Use token as cache key for faster access in
                    user_datastore.set_token(current_app.cache, token, "ADMIN")
                    # each token comparisson
                    # For the admin give only a header, as it is a REST client
                    resp = jsonify({"message": "login succesful"})
                    resp.set_cookie("x-auth", token)
                    return resp

            raise exceptions.InvalidRequest("Invalid login request, wrong credentials", status_code=401)

    @flask_app.route("/auth/client_id")
    def auth_client_id():
        client_id = current_app.private_consts.FenixApi.FENIX_API_CLIENT_ID
        redirect_url = url_for("auth_login", _external=True)

        return jsonify({"client_id": client_id, "redirect_url": redirect_url})
