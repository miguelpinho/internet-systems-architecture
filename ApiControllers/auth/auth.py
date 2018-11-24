from flask import Flask, request


def decorate_auth_handlers(flask_app: Flask):
    @flask_app.route("/auth/login", methods=["GET", "POST"])
    def auth_login():
        if request.method == "GET":
            # Receives Code from fenix api in the args, uses it to get user info
            code = request.args.get("code")
            # Need to be called from fenix oauth redirection as a GET

        else:
            # Receives password and admin name in the POST body
            pass

        return "{'msg':'Login Resource'}"