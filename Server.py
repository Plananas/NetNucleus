import socket
import threading
from Server.ClientHandler import ClientHandler

class Server:

    def __init__(self, port=50000):
        # all the attributes of the server
        self.PORT = port
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.ActiveConnections = 0
        self.clients = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):

        self.server.bind(self.ADDR)
        self.server.listen()
        print(f"server is listening on {self.SERVER}\n")

        while True:
            conn, addr = self.server.accept()
            print(conn)
            print(addr)
            clientHandler = ClientHandler(addr, conn, self)
            self.clients.append(clientHandler)
            handleclientThread = threading.Thread(target=clientHandler.handle_client)
            handleclientThread.start()
            self.ActiveConnections += 1

            print(f"Users Connected: {self.ActiveConnections}")

# let's start the server!
print("[STARTING]")
theServer = Server()
theServer.run()