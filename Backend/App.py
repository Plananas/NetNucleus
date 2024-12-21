from flask import Flask, jsonify

from Repositories.ClientRepository import ClientRepository
from ServerProcess import ServerProcess
import threading


app = Flask(__name__)

@app.route('/clients', methods=['GET'])
def get_clients():
    """Endpoint to return the list of clients."""
    client_repository = ClientRepository()

    # Convert list of ClientModel instances to list of dictionaries
    clients = [client.to_dict() for client in client_repository.get_all_clients()]

    return jsonify(clients), 200


@app.route('/clients/name/<string:client_name>', methods=['GET'])
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

    app.run(debug=True)
