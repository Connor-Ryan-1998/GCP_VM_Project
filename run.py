# # -*- coding: utf-8 -*-
from Controller.app import app

application = app.server
if __name__ == '__main__':
    application.run()
