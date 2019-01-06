from functools import wraps

from flask import g, redirect, request, url_for, current_app

import DbInterface.bots as bot_datastore
import ApiControllers.Auth.exceptions as exceptions
from DbInterface.user import get_token
from Utils.consts import AuthType
from ApiControllers.ApiUtils.db import get_db


def auth_verification(auth_type=AuthType.AUTH_TYPE_USER):
    def decorator_auth_verification(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Fetch db from g object
            db = get_db()

            if auth_type == AuthType.AUTH_TYPE_USER:
                cookie = request.cookies.get("x-auth")
                user_id = get_token(current_app.cache, cookie)

                if user_id is None:
                    # If not in db redirect user to login
                    return redirect(url_for('login', next=request.url))

                g.auth_params = {"user_id": user_id}
                return f(*args, **kwargs)

            elif auth_type == AuthType.AUTH_TYPE_ADMIN:
                # Same as for user, but do not redirect, because admin does not login from a web client
                token = request.headers.get("x-auth", None)
                admin_id = get_token(current_app.cache, token)

                if admin_id is None:
                    # If not in db redirect user to login
                    raise exceptions.InvalidRequest("Not authenticated", status_code=401)

                g.auth_params = {"admin_id": admin_id}
                return f(*args, **kwargs)

            else:  # AUTH_TYPE_BOT
                try:
                    token = request.json()["token"]
                except KeyError:
                    raise exceptions.InvalidRequest("Not a valid token", status_code=401)

                bid = bot_datastore.where_is_bot(db, token, cache=current_app.cache)
                if bid is None:
                    raise exceptions.InvalidRequest("Not a valid token", status_code=401)

                g.auth_params = {"bot_id": token, "bot_building": bid}
                return f(*args, **kwargs)

        return decorated_function

    return decorator_auth_verification
