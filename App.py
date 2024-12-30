import threading

from flask import Flask

from Backend.App.Controllers.ClientController import ClientController
from ServerProcess import ServerProcess


global server

if __name__ == '__main__':
    client_controller = ClientController()

    threading.Thread(target=client_controller.server.run, daemon=True).start()

    app = Flask(__name__, static_folder='Frontend/static', template_folder='frontend/templates')
    blueprint = client_controller.getBlueprint()
    app.register_blueprint(blueprint)
    app.run(debug=True)
