from flask import Flask, jsonify
from flask import Blueprint, render_template

from Backend.App.Repositories.ClientRepository import ClientRepository
from Backend.App.Repositories.InstalledProgramRepository import InstalledProgramRepository
from Backend.App.ServerProcess import ServerProcess
import threading


main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

@main.route('/api/clients', methods=['GET'])
def get_clients():
    """Endpoint to return the list of clients."""
    client_repository = ClientRepository()

    # Convert list of ClientModel instances to list of dictionaries
    clients = [client.to_dict() for client in client_repository.get_all_clients()]

    return jsonify(clients), 200

@main.route('/clients', methods=['GET'])
def get_clients_page():
    """Endpoint to return the list of clients."""
    client_repository = ClientRepository()

    # Convert list of ClientModel instances to list of dictionaries
    clients = [client.to_dict() for client in client_repository.get_all_clients()]

    return render_template('clients.html', clients=clients)


@main.route('/clients/<string:mac_address>', methods=['GET'])
def get_client_by_mac_page(mac_address):
    """Endpoint to return a single client by name."""
    client_repository = ClientRepository()
    program_repository = InstalledProgramRepository()

    # Attempt to retrieve the client by nickname
    client = client_repository.get_client_by_mac_address(mac_address)[0]

    # Convert list of ClientModel instances to list of dictionaries
    programs = [program.to_dict() for program in client.get_installed_programs()]

    if client is None:
        return jsonify({"error": f"No client found with nickname '{mac_address}'"}), 404

    # Convert the client to a dictionary
    return render_template('client.html', client=client, programs=programs)


@main.route('/api/clients/name/<string:client_name>', methods=['GET'])
def get_client_by_name(client_name):
    """Endpoint to return a single client by name."""
    client_repository = ClientRepository()

    # Attempt to retrieve the client by nickname
    client = client_repository.get_client_by_nickname(client_name)

    if client is None:
        return jsonify({"error": f"No client found with nickname '{client_name}'"}), 404

    # Convert the client to a dictionary
    return jsonify(client.to_dict()), 200


if __name__ == '__main__':

    # Create a thread for the server's run method
    server_thread = threading.Thread(target=ServerProcess().run).start()
    app = Flask(__name__, static_folder='Frontend/static', template_folder='frontend/templates')
    app.register_blueprint(main)  # Register the blueprint to the app
    app.run(debug=True)
