from flask import Flask, jsonify


class NotAuthenticated(Exception):
    status_code = 403  # Not Authorized

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def decorate_error_handlers(flask_app : Flask):
    # Error Handle for Invalid Requests
    @flask_app.errorhandler(NotAuthenticated)
    def handle_not_authenticated(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response