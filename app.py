from flask import Flask, g
import ApiControllers
from DbClient.db import close_db, init_db, get_db
from QueueInterface.exchange import create_exchanges
from QueueInterface.logs import create_logs_queues
from Utils.consts import configure_private_consts

app = Flask(__name__)

# Set private consts
private_consts = configure_private_consts()
app.private_consts = private_consts

# Instantiate socketio interface
sio_class = ApiControllers.Sockio(private_consts)
sio = sio_class.config_socketio(app)

# Instantiate database
init_db(get_db())

# Instantiate db_interfaces

# Create message queue exchanges
create_exchanges(private_consts)
# Create message queues for logs
create_logs_queues(private_consts)

# Instantiate all the APIs with the db_interface passed in the second
ApiControllers.decorate_web_app(app)
ApiControllers.decorate_user_routes(app)
ApiControllers.decorate_bot_routes(app)
ApiControllers.decorate_admin_routes(app)
ApiControllers.decorate_auth_handlers(app)

# Instantiate the error handlers
ApiControllers.decorate_error_handlers(app)
ApiControllers.decorate_auth_error_handlers(app)


# Configure app context teardown
@app.teardown_appcontext
def request_teardown(e):
    # Close request db connection
    db = g.pop("db", None)
    if db is not None:
        close_db(db)
    # Close request fenix connection
    if "fenix" in g:
        g.pop("fenix")


if __name__ == '__main__':
    sio.run(app)
