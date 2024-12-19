import socket
from typing import List
import threading
import time
from Models.Message import Message

class Server:

    def __init__(self, port=50000):
        # all the attributes of the server
        self.PORT = port
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.ActiveConnections = 0
        self.clients: List[Message] = []
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
            client = Message(conn)
            self.clients.append(client)
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
                for index, client in enumerate(self.clients):
                    try:
                        print(index)
                        client.write(message)
                        print(f"[SENT] Message sent to client {index}")
                    except (socket.error, ConnectionResetError):
                        print(f"\n[CONNECTION ERROR] Client {index} disconnected.")
                        client.connection.close()
                        self.clients.remove(client)
                        self.ActiveConnections -= 1
        except KeyboardInterrupt:
            print("\n[INFO] Interrupted by user. Exiting.")

# let's start the server!
print("[STARTING]")
theServer = Server()
theServer.run()