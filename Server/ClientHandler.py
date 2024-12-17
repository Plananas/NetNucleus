from Models.Message import Message
import time

from Server.State import State


class ClientHandler:
    def __init__(self, _addr, _conn, _device):
        # all the client's attributes
        self.currentState = State.Start
        self.DISCONNECT_MESSAGE = "goodbye"
        self.addr = _addr
        self.conn = _conn
        self.message = 0
        self.connected = False
        self.device = _device
        self.count = 0


    def handle_client(self):
        addr = self.addr
        conn = self.conn
        self.log(f"{addr} has connected")
        print(f"{addr} has connected")

        # Message Handler deals with all the message sending.
        self.message = Message(conn)

        # We only want to do this stuff while a user is connected.
        self.connected = True
        while self.connected:
            try:

                msg = self.receive()
                print(f"Received {msg}")
                # Our message handlers
                if msg == self.DISCONNECT_MESSAGE:
                    self.log(f"user {addr} has disconnected")
                    print(f"user {addr} has disconnected")
                    self.connected = False
                else:
                    # Handle simple states with client->server, server-> client pattern
                    if self.currentState == State.Start:
                        msg = self.start(msg)
                    else:
                        msg = self.handleError(msg)

                    self.send(msg)
            except:
                self.log(f"error with client {addr}")
                print(f"error with client {addr}")
                break
        # removes us from the connected clients list
        self.device.clients.remove(self)
        self.device.ActiveConnections -= 1
        conn.close()

    # this is the state once the user has logged in and is choosing the options.
    def start(self, message):
        if not message:
            message = self.handleError("That was not a valid command")

        return message

    # This will make sure an error is sent back to the user telling them what went wrong.
    # returns them to start to try again.
    def handleError(self, message):
        self.currentState = State.Start
        self.previousState = State.Error
        self.log(f"--Error: {message}")
        return f"--Error: {message}"

    # this sends the message to the message handler.
    def send(self, msg):
        self.message.write(msg)

    # grabs an incoming message from the message handler.
    def receive(self):
        message = self.message.read()
        self.log(message)

        return message


    def log(self, msg):
        print(msg)