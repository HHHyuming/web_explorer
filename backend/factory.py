from flask import Flask, current_app
from flask_cors import CORS

import config
from api.explorer import blue_explorer
from api.login import blue_user_action


def create_app(env):
    app = Flask(__name__, static_folder=config.STATIC_FOLDER)
    # 加载配置文件
    if env == 'development':
        app.config.from_object(config.config_map['development'])
    if env == 'production':
        app.config.from_object(config.config_map['production'])

    # load redis-api

    # load api
    app.register_blueprint(blue_user_action)
    app.register_blueprint(blue_explorer)
    # 跨域配置

    CORS(app)
    return app