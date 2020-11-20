'''
Registers blueprints with respective url_prefixes.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from app_.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error

from flask import Flask

from route import admin_route, auth_route, channels_route, channel_route, search_route, \
    users_route, user_route, standup_route, workspace_route, message_route, profileimages_route,\
        hangman_route


APP = Flask(__name__)

#### REGISTER BLUEPRINTS
APP.register_blueprint(channel_route.MOD_CHANNEL, url_prefix='/channel')
APP.register_blueprint(standup_route.MOD_STANDUP, url_prefix='/standup')
APP.register_blueprint(admin_route.MOD_ADMIN, url_prefix='/admin')
APP.register_blueprint(message_route.MOD_MESSAGE, url_prefix='/message')
APP.register_blueprint(channels_route.MOD_CHANNELS, url_prefix='/channels')
APP.register_blueprint(workspace_route.MOD_WORKSPACE, url_prefix='/workspace')
APP.register_blueprint(auth_route.MOD_AUTH, url_prefix='/auth')
APP.register_blueprint(user_route.MOD_USER, url_prefix='/user')
APP.register_blueprint(users_route.MOD_USERS, url_prefix='/users')
APP.register_blueprint(search_route.MOD_SEARCH) # No url prefix required for this BP.
APP.register_blueprint(profileimages_route.MOD_PROFILEIMAGES, url_prefix='/profileimages')
APP.register_blueprint(hangman_route.MOD_HANG, url_prefix='/hangman')
