from flask import Flask
import ApiControllers

app = Flask(__name__)

# Instantiate database

# Instantiate db_interfaces

# Instantiate all the APIs with the db_interface passed in the second
ApiControllers.decorate_web_app(app)
ApiControllers.decorate_user_routes(app)
ApiControllers.decorate_bot_routes(app)
ApiControllers.decorate_admin_routes(app)
ApiControllers.decorate_auth_handlers(app)

# Instantiate the error handlers
ApiControllers.decorate_error_handlers(app)
ApiControllers.decorate_auth_error_handlers(app)

if __name__ == '__main__':
    app.run()
