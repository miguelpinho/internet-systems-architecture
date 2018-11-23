# Admin

An admin can manage buildings and bots on the system and has
access to the users connected and all the logs.

## /api/admin/bots

Add, list or remove bots. The bot is both authenticated
and identified by an auth token.

- POST /api/admin/bots/{building}
    - receives: building
    - returns:
        - token
        - 200 OK
    - produces: adds bot to database
    - fails:

- DELETE /api/admin/bots/{token}
    - receives: auth token
    - returns:
        - token
        - 200 OK
    - produces: removes bot from database
    - fails:

- GET /api/admin/bots/
    - returns:
        - list of all bots
        - 200 OK
    - fails:

- GET /api/admin/bots/{building}
    - receives: building
    - returns:
        - list of all bots in that building
        - 200 OK
    - fails:

- GET /api/admin/bots/{token}/building
    - receives: auth token
    - returns:
        - list the building of that bot
        - 200 OK
    - fails:

## /api/admin/buildings

- POST /api/admin/buildings/{id}
    - receives: id, name, latitude, longitude
    - returns:
        - 200 OK
    - produces: adds building to the database
    - fails:

- DELETE /api/admin/buildings/{id}
    - receives: id
    - returns:
        - id
        - 200 OK
    - produces: removes building from database
    - fails:

- GET /api/admin/buildings/
    - returns:
        - list of all buildings
        - 200 OK
    - fails:

- GET /api/admin/buildings/{id}
    - receives: id
    - returns:
        - building data
        - list of users
        - 200 OK
    - fails:

## /api/admin/logs

- GET /api/admin/logs/users/{istID}/moves
    - receives: istID
    - returns:
        - log of moves for that user
        - 200 OK
    - fails:

- GET /api/admin/logs/users/{istID}/messages
    - receives: istID
    - returns:
        - log of messages for that user
        - 200 OK
    - fails:

- GET /api/admin/logs/buildings/{id}
    - receives: id
    - returns:
        - log of messages from bots in a building
        - 200 OK
    - fails:


# User

A user can set his location and radius, and receive and
send messages. Authentication using Fenix is required.

## /api/user

- GET /api/user/messages
    - receives: oauth token
    - returns:
        - received messages list
        - 200 OK
    - fails:

- POST /api/user/messages
    - receives: oauth token; message
    - returns:
        - 200 OK
    - produces: store message in other users' queue
    - fails:

- POST /api/user/location
    - receives: oauth token; position (lat, long)
    - returns:
        - 200 OK
    - produces: updates location
    - fails:

- GET /api/user/building
    - receives: oauth token
    - returns:
        - current building
        - 200 OK
    - fails:

- POST /api/user/radius
    - receives: oauth token; radius
    - returns:
        - 200 OK
    - produces: changes proximity radius
    - fails:

- GET /api/user/nearby
    - receives: oauth token
    - returns:
        - list of users nearby
        - 200 OK
    - fails:


# Bot

Only sends messages, to the building with was registered on
by the admin. Requires the usage of a token, which identifies
it.

## /api/bot

- POST /api/bot/{token}
    - receives: oauth token; message
    - returns:
        - 200 OK
    - produces: sends messages to users in the bot's building
    - fails:


# Home

WebApp, which enables logged users to access a dashboard where
they can read the messages received and send theirs.

- /
    - redirects to login

- /login
    - redirects to fenix authentication
    - receives oauth code
    - redirects to dashboard on success

- /dashboard
    - set location/radius ??
    - show info: building, nearby users
    - show received message
    - send new messages
