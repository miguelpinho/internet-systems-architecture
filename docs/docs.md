# Admin

An admin can manage buildings and bots on the system and has
access to the users connected and all the logs.
## Admin Api (/api/admin)

## » Admin Api > Bots

Add, list or remove bots. The bot is both authenticated
and identified by an auth token.

### »» /api/admin/bots/
#### GET
    - returns:
        - List of all bots
        - 200 OK
    - fails:

#### POST   
    - receives(Body): building
    - returns:
        - Token
        - 200 OK
    - produces: adds bot to database
    - fails:

***
### »» /api/admin/bots/{token}
#### GET
    - returns:
        - Bot Information: Building and others
        - 200 OK
    - fails:

#### DELETE
    - returns:
        - Token
        - Bot Information
        - 200 OK
    - produces: removes bot from database
    - fails:

***
***
## » Admin Api > Buildings

### »» /api/admin/buildings/
#### POST
    - receives (body): id, name, latitude, longitude
    - returns:
        - 200 OK
    - produces: adds building to the database
    - fails:
#### GET
	- returns:
        - list of all buildings (name and id)
        - 200 OK
    - fails:

***
### »» /api/admin/buildings/{bid}
#### DELETE
    - returns:
        - Building Info
        - 200 OK
    - produces: removes building from database
    - fails:
#### GET
    - returns:
        - Building Info
        - List of Users
        - List of Bots
        - 200 OK
    - fails:

***
***

## » Admin Api > Logs

### »» /api/admin/logs/users/{istID}/moves
#### GET
    - returns:
        - log of moves for that user
        - 200 OK
    - fails:
***
### »» /api/admin/logs/users/{istID}/messages
#### GET
    - returns:
        - log of messages for that user
        - 200 OK
    - fails:
***
### »» /api/admin/logs/buildings/{bid}
#### GET
    - returns:
        - log of messages from bots in a building
        - 200 OK
    - fails:
***
***

# User

A user can set his location and radius, and receive and
send messages. Authentication using Fenix is required.

## » User Api (/api/user)
All of the below require user authentication, user should pass in the header the authentication token provided by the server.

### »» /api/user/messages
#### GET
    - returns:
        - received messages list
        - 200 OK
    - fails:
#### POST
    - receives (body): message
    - returns:
        - 200 OK
    - produces: store message in other users' queue
    - fails:
***
### »» /api/user/location
#### POST
    - receives (body): position (lat, long)
    - returns:
        - 200 OK
    - produces: updates location
    - fails:
***
### »» /api/user/building
#### GET
    - returns:
        - current building
        - 200 OK
    - fails:
***
### » /api/user/radius
#### POST
    - receives (body): radius
    - returns:
        - 200 OK
    - produces: changes proximity radius
    - fails:
***
### » /api/user/nearby
#### GET
    - returns:
        - list of users nearby
        - 200 OK
    - fails:
***
***

# Bot

Only sends messages, to the building with was registered on
by the admin. Requires the usage of a token, which identifies
it, this should be passed in the header in the same way as an user.

## » Bot Api (/api/bot)

### »» /api/bot/{token}
#### POST
    - receives (body): message
    - returns:
        - 200 OK
    - produces: sends messages to users in the bot's building
    - fails:
***
***

# Auth

Provides a interface for authentication, for users (fenix api) and admin (local)

## » Auth Api (/auth)

### »» /auth/login
#### GET
    Used for fenix api authentication (user) 
    - receives (query): fenix api code
    - returns:
        - 200 OK
        - Auth Header
    - produces: logs in the user
    - fails: 400 Bad Request or 403 Not Authorized
#### POST
    Used for local authentication (admin)
    - receives (body): admin username, admin password
    - returns:
        - 200 OK
        - Auth Header
    - produces: logs in the admin
    - fails: 400 Bad Request or 403 Not Authorized
***
***

# Home

Web App, which enables logged users to access a dashboard where
they can read the messages received and send theirs.

## root (/)
    - Simple web page that explains the app (Hint: This web page)
    - Can provide the api docs
    - Has a simple login button that redirects to fenix api

## dashboard (/dashboard)
    User client for the api
    Provides a interface that is able to:
    - Set location and radius
    - Show info: Current building, Nearby users
    - Show received messages
    - Send new messages
***