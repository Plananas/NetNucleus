import socket
import threading
from typing import List

from flask import Flask, jsonify, request
from flask import Blueprint, render_template

from Backend.App.Repositories.ClientRepository import ClientRepository
from Backend.App.Repositories.ProgramRepository import ProgramRepository
from Backend.App.Server.ClientHandler import ClientHandler


class ClientController:

    main = Blueprint(
            "main",
            __name__,
            static_folder="Frontend/static",
            template_folder="frontend/templates"
    )

    def __init__(self):
        self.clientHandlers: List[ClientHandler] = []
        # Bind the instance method to the route
        self.main.add_url_rule(
            '/api/clients/shutdown',
            'shutdown_client',
            self.shutdown_client,
            methods=['POST']
        )
        self.lock = threading.Lock()

    def getBlueprint(self):
        return self.main

    def updateClientHandlers(self, clientHandlers: ClientHandler):
        print('ADDING CLIENT HANDLERS')
        self.clientHandlers.append(clientHandlers)


    @staticmethod
    @main.route('/')
    def home():
        """Render the home page."""
        return render_template('home.html')


    @staticmethod
    @main.route('/api/clients', methods=['GET'])
    def get_clients():
        """Endpoint to return the list of clients."""
        client_repository = ClientRepository()

        # Convert list of ClientModel instances to list of dictionaries
        clients = [client.to_dict() for client in client_repository.get_all_clients()]

        return jsonify(clients), 200


    @staticmethod
    @main.route('/clients', methods=['GET'])
    def get_clients_page():
        """Endpoint to return the list of clients."""
        client_repository = ClientRepository()

        # Convert list of ClientModel instances to list of dictionaries
        clients = [client.to_dict() for client in client_repository.get_all_clients()]

        return render_template('clients.html', clients=clients)


    @staticmethod
    @main.route('/clients/<string:mac_address>', methods=['GET'])
    def get_client_by_mac_page(mac_address):
        """Endpoint to return a single client by name."""
        client_repository = ClientRepository()
        program_repository = ProgramRepository()

        # Attempt to retrieve the client by nickname
        client = client_repository.get_client_by_mac_address(mac_address)[0]

        # Convert list of ClientModel instances to list of dictionaries
        programs = [program.to_dict() for program in client.get_installed_programs()]

        if client is None:
            return jsonify({"error": f"No client found with nickname '{mac_address}'"}), 404

        # Convert the client to a dictionary
        return render_template('client.html', client=client, programs=programs)


    @staticmethod
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

    def shutdown_client(self):
        print("SHUTDOWN ENDPOINT TRIGGERED")
        data = request.get_json()
        if 'mac_address' not in data:
            return jsonify({"error": "No MAC address provided."}), 400

        mac_address = data['mac_address']
        client_repository = ClientRepository()

        client = client_repository.get_client_by_mac_address(mac_address)
        if not client:
            return jsonify({"error": f"No client found with mac address: '{mac_address}'"}), 404

        client = client[0]  # Assuming the repository returns a list

        for index, clientHandler in enumerate(self.clientHandlers):
            print(clientHandler)

        return jsonify({"message": "", "active_connections": "active_connections"}), 200
