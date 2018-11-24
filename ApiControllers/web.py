from flask import render_template

from ApiControllers.exceptions import *


def decorate_web_app(flask_app: Flask):

    @flask_app.route("/")
    def home():
        # Receives Token and Message in POST body
        return render_template("root.html")

    @flask_app.route("/dashboard")
    def dashboard():
        # Receives Token and Message in POST body
        return "<h1>Dashboard</h1>"
