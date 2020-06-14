import os

import config


class StaticResource:
    def __init__(self, users):
        self.users = users

    def load(self):
        for user in self.users:
            user_static_folder = os.path.join(config.STATIC_FOLDER, user)

            os.mkdir(user_static_folder)
