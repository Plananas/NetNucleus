import socket
from getmac import get_mac_address
import Backend.App.Client.SystemFunctions as SystemFunctions
from Backend.App.Models.MessageController import MessageController
import time

class Client:
    def __init__(self):
        # all the client's attributes
        self.PORT = 50000
        #print("Input the address of the server")
        #self.SERVER = input("> ")
       # self.SERVER = "10.130.94.3"
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.message = MessageController(object)
        self.Connected = False

        # Create the client socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set larger buffer sizes
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)  # 64 KB for sending
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)


        self.macAddress = get_mac_address()

    def run(self):
        try:
            self.client.connect(self.ADDR)
        except:
            print("[CONNECTION ERROR]Could not connect to host.\nEither the host isn't up or your not connected to the network.")

        try:
            #Message handler will deal with the sending of all messages.
            self.message = MessageController(self.client)
            self.Connected = True

        except:
            print("Error creating the message Handler")
            self.Connected = False

        self.handleServer()

    def handleServer(self):
        print("\n[LISTENING FOR MESSAGES]")
        # Constantly listening to the server for messages.
        while self.Connected:
            try:
                msg = self.message.read()

                try:
                    print("[READING MESSAGE]", msg)
                    self.send(self.processMessage(msg))
                except:
                    print("Error processing message")
            except:
                print("\n[CONNECTION ERROR] Disconnecting")
                self.connected = False
                break
            print(f"{msg}")

    # this will send our message into the message handler
    def send(self, msg):
        time.sleep(0.5)
        if msg == "":
            # empty strings caused my encryption to give out bad results so ive added this to the client
            print("please dont send empty strings... it breaks the server.")
        else:
            write = self.message.write({self.macAddress: msg})

    def processMessage(self, message):
        print("\n[MESSAGE PROCESSING]")
        if message.lower() == "shutdown":
            return SystemFunctions.shutdown()
        if message.lower() == "upgrades":
            return SystemFunctions.getUpdatableSoftware()
        if message.lower() == "software":
            return SystemFunctions.getAllSoftware()

# let's run out client!!!!
client = Client()
client.run()
