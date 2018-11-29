from functools import wraps
from flask import g, redirect, request, url_for

from ApiControllers.auth.exceptions import NotAuthenticated
from Utils.consts import AuthType


def auth_verification(auth_type=AuthType.AUTH_TYPE_USER):
    def decorator_auth_verification(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Fetch db from g object

            if auth_type == AuthType.AUTH_TYPE_USER:
                # Verify user based on token (may be in the header or somewhere), check it in database (get_db())

                # If not in db:
                #    raise unauthorized error:  raise NotAuthenticated
                # or redirect user to login:    return redirect(url_for('login', next=request.url))
                pass

            elif auth_type == AuthType.AUTH_TYPE_ADMIN:
                # Same as for user, but do not redirect, because admin does not login from a web client
                pass

            else:  # AUTH_TYPE_BOT
                # Check bot token in db
                pass

            # If user/admin/bot is logged in, go get the user uuid in the database, then pass it to the next handler
            # in g.auth_params.uuid
            g.auth_params = {"uuid": "Fake UUID"}

            return f(*args, **kwargs)

        return decorated_function

    return decorator_auth_verification
