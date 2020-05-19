from flask import Flask
from flask_cors import CORS

import config
from api.explorer import blue_explorer
from api.login import blue_user_action


def create_app(env):
    app = Flask(__name__)
    # 加载配置文件
    if env == 'development':
        app.config.from_object(config.config_map['development'])
    if env == 'production':
        app.config.from_object(config.config_map['production'])

    # 跨域配置
    CORS(app)
    # load api
    app.register_blueprint(blue_user_action)
    app.register_blueprint(blue_explorer)
    return app