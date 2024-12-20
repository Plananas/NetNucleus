import socket
from typing import List
import threading
import time

from Models.ClientModel import ClientModel
from Models.MessageController import MessageController
from Server.ClientHandler import ClientHandler


class Server:

    def __init__(self, port=50000):
        # all the attributes of the server
        self.PORT = port
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.ActiveConnections = 0
        self.clients: List[ClientHandler] = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):

        self.server.bind(self.ADDR)
        self.server.listen()
        print(f"server is listening on {self.SERVER}\n")
        threading.Thread(target=self.clientController).start()

        while True:
            conn, addr = self.server.accept()
            print(conn)
            print(addr)
            clientHandler = ClientHandler(MessageController(conn))
            self.clients.append(clientHandler)
            self.ActiveConnections += 1
            print(f"Users Connected: {self.ActiveConnections}")

    def clientController(self):
        try:
            while True:
                time.sleep(0.5)
                message = input("> ")

                if message.lower() == "exit":

                    print("\n[INFO] Exiting client controller.")
                    break

                # Add a slight delay to let the server process
                time.sleep(1)

                # Send the message to each client in the list
                self.broadcast(message)
        except KeyboardInterrupt:
            print("\n[INFO] Interrupted by user. Exiting.")

    def broadcast(self, message):
        """
        Broadcast to every connected client
        :param message:
        :return:
        """

        for index, clientHandler in enumerate(self.clients):
            try:
                print(self.processMessage(message, clientHandler))
                # TODO for that client we need to process what happened

            except (socket.error, ConnectionResetError):
                print(f"\n[CONNECTION ERROR] Client {clientHandler.messageController.messageId} disconnected.")
                clientHandler.messageController.connection.close()
                self.clients.remove(clientHandler)
                self.ActiveConnections -= 1

    def processMessage(self, message, clientHandler):
        print("\n[MESSAGE PROCESSING]")
        if message.lower() == "shutdown":
            return clientHandler.shutdown()
        elif message.lower() == "upgrades":
            return clientHandler.getUpdate()
        elif message.lower() == "software":
            return clientHandler.getAllSoftware()

# let's start the server!
print("[STARTING]")
theServer = Server()
theServer.run()