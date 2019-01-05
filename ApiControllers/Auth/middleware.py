from functools import wraps
from flask import g, redirect, request, url_for, current_app

from ApiControllers.Auth.exceptions import NotAuthenticated
from Utils.consts import AuthType
from db import get_db
from DbInterface.user import get_userid_from_cookie


def auth_verification(auth_type=AuthType.AUTH_TYPE_USER):
    def decorator_auth_verification(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Fetch db from g object
            db = get_db()

            if auth_type == AuthType.AUTH_TYPE_USER:
                cookie = request.cookies.get("x-auth")
                user_id = get_userid_from_cookie(db, cookie)

                if user_id is None:
                    # If not in db redirect user to login
                    return redirect(url_for('login', next=request.url))

                g.auth_params = {"user_id": user_id}
                return f(*args, **kwargs)

            elif auth_type == AuthType.AUTH_TYPE_ADMIN:
                # TODO: Check admin token in db
                # Same as for user, but do not redirect, because admin does not login from a web client
                admin_id = "Some Admin"
                g.auth_params = {"admin_id": admin_id}
                return f(*args, **kwargs)

            else:  # AUTH_TYPE_BOT
                # TODO: Check bot token in db
                bot_id = "Some bot"
                g.auth_params = {"bot_id": bot_id}
                return f(*args, **kwargs)

        return decorated_function

    return decorator_auth_verification
