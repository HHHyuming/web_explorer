import platform
from factory import create_app


if platform.system() == 'Windows':
    application = create_app(env='development')
    application.run()

if platform.system() == 'Linux':
    pass