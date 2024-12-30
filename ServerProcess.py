import socket
from typing import List
import re
import threading
import time

from Backend.App.Models.MessageController import MessageController
from Backend.App.Repositories.ClientRepository import ClientRepository
from Backend.App.Server.ClientHandler import ClientHandler
from flask import Flask
from Backend.App.Controllers.ClientController import ClientController


class ServerProcess:
    PORT = 50000

    def __init__(self):
        self.client_controller = None
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.active_connections = 0
        self.client_handlers: List[ClientHandler] = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_controller = ClientController()
        self.lock = threading.Lock()


    def run(self):

        self.server.bind(self.ADDR)
        self.server.listen()
        print(f"server is listening on {self.SERVER}\n")
        threading.Thread(target=self.terminal_process, daemon=True).start()
        threading.Thread(target=self.search_for_clients, daemon=True).start()

        #TODO set existing clients to shutdown
        client_repository = ClientRepository()
        clients = client_repository.get_all_clients()
        for client in clients:
            client.set_shutdown(True)
            client.save()

        app = Flask(__name__, static_folder='Frontend/static', template_folder='frontend/templates')
        blueprint = self.client_controller.getBlueprint()
        app.register_blueprint(blueprint)
        app.run(debug=True)


    def search_for_clients(self):
        while True:
            conn, addr = self.server.accept()
            print(conn)
            print(addr)
            clientHandler = ClientHandler(MessageController(conn))
            with self.lock:
                self.client_handlers.append(clientHandler)
                self.active_connections += 1
                self.client_controller.updateClientHandlers(clientHandler)
            print(f"Users Connected: {self.active_connections}")


    def terminal_process(self):
        try:
            while True:
                time.sleep(0.5)
                message = input("> ")

                if message.lower() == "exit":
                    print("\n[INFO] Exiting client controller.")
                    break

                # Check if the message contains exactly two words
                splitMessage = message.split()
                if len(splitMessage) >= 2 and self.is_valid_uuid(splitMessage[-1]):
                    self.send_to_client(splitMessage, splitMessage[-1])
                else:
                    # Add a slight delay to let the server process
                    time.sleep(1)

                    # Send the message to each client in the list
                    self.broadcast(splitMessage)
        except KeyboardInterrupt:
            print("\n[INFO] Interrupted by user. Exiting.")


    def broadcast(self, message):
        """
        Broadcast to every connected client
        :param message:
        :return:
        """

        for index, client_handler in enumerate(self.client_handlers):
            try:
                print(self.process_messages(message, client_handler))

            except (socket.error, ConnectionResetError):
                print(f"\n[CONNECTION ERROR] Client {client_handler.messageController.messageId} disconnected.")
                client_handler.messageController.connection.close()
                client_handler.set_shutdown()
                self.client_handlers.remove(client_handler)
                self.active_connections -= 1


    def send_to_client(self, message, uuid):
        """
        Send to a Specific Client
        :param uuid:
        :param message:
        :return:
        """
        clientRepository = ClientRepository()
        client = clientRepository.get_client_by_uuid(uuid)[0]

        # Find the ClientHandler object with the same MAC address as the repository object
        client_handler = next(
            (handler for handler in self.client_handlers if handler.clientModel.get_uuid() == client.get_uuid()),
            None
        )
        print(self.active_connections)
        for clientHandler in self.client_handlers:
            print(clientHandler.clientModel.get_uuid())

        if client_handler:
            print(client.get_uuid())
            try:
                client = self.process_messages(message, client_handler)
                print(client.get_uuid())

            except (socket.error, ConnectionResetError):
                print(f"\n[CONNECTION ERROR] Client {client_handler.messageController.messageId} disconnected.")
                client_handler.messageController.connection.close()
                client_handler.set_shutdown()
                self.client_handlers.remove(client_handler)
                self.active_connections -= 1


    def process_messages(self, message, client_handler):
        print("\n[MESSAGE PROCESSING]")
        if message:
            if message[0].lower() == "shutdown":
                return client_handler.shutdown()
            elif message[0].lower() == "upgrades":
                return client_handler.get_available_updates()
            elif message[0].lower() == "software":
                return client_handler.get_client_with_software()
            elif message[0].lower() == "upgrade":
                return client_handler.upgrade_all_software()
            elif message[0].lower() == "terminated":
                return client_handler.terminate()

            if len(message) >= 2:
                if message[0].lower() == "install":
                    return client_handler.install_software(message[1])
                elif message[0].lower() == "uninstall":
                    return client_handler.uninstall_software(message[1])
                elif message[0].lower() == "upgrade":
                    return client_handler.upgrade_software(message[1])
        else:
            print("enter a valid message")


    @staticmethod
    def is_valid_uuid(uuid_str):
        # Regular expression for matching UUID format
        uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        return bool(re.match(uuid_pattern, uuid_str))