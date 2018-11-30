from flask import Flask, request, jsonify, url_for, render_template

from Utils.private_consts import FENIX_API_CLIENT_ID


def decorate_auth_handlers(flask_app: Flask):
    @flask_app.route("/auth/login", methods=["GET", "POST"])
    def auth_login():
        if request.method == "GET":
            # Receives Code from fenix api in the args, uses it to get user info
            code = request.args.get("code")
            print(code)
        else:
            # Receives password and admin name in the POST body
            pass

        return render_template("dashboard.html")

    @flask_app.route("/auth/client_id")
    def auth_client_id():
        client_id = FENIX_API_CLIENT_ID
        redirect_url = url_for("auth_login", _external=True)

        return jsonify({"client_id": client_id, "redirect_url": redirect_url})
