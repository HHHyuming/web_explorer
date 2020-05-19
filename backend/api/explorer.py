from flask import Blueprint

blue_explorer = Blueprint('explorer', __name__, url_prefix='/explorer')


@blue_explorer.before_request
def check_user_legal():
    """
    jwt 验证
    :return:
    """
    pass


