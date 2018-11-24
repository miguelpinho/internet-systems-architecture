from functools import wraps
from flask import g, redirect, request, url_for

from ApiControllers.auth.exceptions import NotAuthenticated


def auth_verification():  # This is not needed, but can receive some parameters for configuration of auth
    def decorator_auth_verification(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verify user based on token (may be in the header or somewhere)

                # If not redirect or raise unauthorized error
                # return redirect(url_for('login', next=request.url))
                # raise NotAuthenticated

            # If user is logged in go get the user uuid in the database, then pass it to the next handler
            # in g.auth_params.uuid
            g.auth_params = {"uuid": "Fake UUID"}
            return f(*args, **kwargs)

        return decorated_function
    return decorator_auth_verification