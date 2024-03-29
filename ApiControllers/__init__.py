from .admin import decorate_admin_routes
from .bot import decorate_bot_routes
from .user import decorate_user_routes
from .exceptions import decorate_error_handlers
from .Auth import decorate_error_handlers as decorate_auth_error_handlers
from .socket_io import Sockio

# noinspection PyUnresolvedReferences
from .Auth import auth_verification
# noinspection PyUnresolvedReferences
from .Auth import decorate_auth_handlers
# noinspection PyUnresolvedReferences
from .web import decorate_web_app

__all__ = [decorate_admin_routes, decorate_bot_routes, decorate_user_routes, decorate_error_handlers,
           decorate_auth_error_handlers, Sockio]
