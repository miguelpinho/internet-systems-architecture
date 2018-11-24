from ApiControllers.exceptions import *


def decorate_web_app(flask_app: Flask):

    @flask_app.route("/")
    def home():
        # Receives Token and Message in POST body
        return "<h1>Main Page</h1>"

    @flask_app.route("/dashboard")
    def dashboard():
        # Receives Token and Message in POST body
        return "<h1>Dashboard</h1>"
