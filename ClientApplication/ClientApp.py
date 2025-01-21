import os
import json
import socket
import time
from getmac import get_mac_address
import SystemFunctions
from MessageController import MessageController
import servicemanager


class Client:
    CONFIG_DIR = os.path.join(os.environ["ProgramData"], "NetworkAutomationClient")
    CONFIG_FILE = os.path.join(CONFIG_DIR, "client.config")  # Full path to the config file
    SERVICE_NAME = "NetworkAutomationClient"
    def __init__(self):
        #check choco is installed or the app won't work
        SystemFunctions.ensure_chocolatey_installed()
        self.PORT = 50000
        self.SERVER = self.get_server_ip()
        self.ADDR = (self.SERVER, self.PORT)
        self.message = MessageController(object)
        self.Connected = False

        # Create the client socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set larger buffer sizes
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)  # 64 KB for sending
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)

        self.macAddress = get_mac_address()


    def get_server_ip(self):
        """Retrieve the server IP from a config file or prompt the user via a UI."""
        try:
            with open(self.CONFIG_FILE, "r") as f:
                for line in f:
                    if line.startswith("IP_ADDRESS="):
                        return line.strip().split("=")[1]
        except FileNotFoundError:
            print("Configuration file not found.")
            return None

    def run(self, servicemanager):
        while True:
            try:
                print(f"Attempting to connect to {self.ADDR}...")
                self.client.connect(self.ADDR)
                print("[CONNECTION SUCCESS] Connected to host.")
                break  # Exit the loop if connection is successful
            except Exception as e:
                print(f"[CONNECTION ERROR] Could not connect to host: {e}")
                print("Retrying in 30 seconds...")
                time.sleep(30)

        try:
            self.message = MessageController(self.client)
            self.Connected = True
            print("[MESSAGE CONTROLLER] Successfully created.")
        except Exception as e:
            print(f"[MESSAGE CONTROLLER ERROR] Error creating the message handler: {e}")
            self.Connected = False

        servicemanager.LogInfoMsg(f"{self.SERVICE_NAME}: Service is now running.")
        self.handle_server()

    def handle_server(self):
        print("\n[LISTENING FOR MESSAGES]")
        while self.Connected:
            try:
                msg = self.message.read()
                if msg:
                    print("[READING MESSAGE]", msg)
                    self.send(self.process_message(msg))
            except socket.timeout:
                # Timeout occurred, check if still running
                continue
            except Exception as e:
                print(f"\n[CONNECTION ERROR] {e}. Disconnecting.")
                self.Connected = False
                break

    def send(self, msg):
        time.sleep(0.5)
        if msg == "":
            print("Please don't send empty strings. It breaks the server.")
        else:
            self.message.write({self.macAddress: msg})

    def process_message(self, message):
        print("\n[MESSAGE PROCESSING]")
        if message.lower() == "shutdown":
            return SystemFunctions.shutdown()
        if message.lower() == "upgrades":
            return SystemFunctions.get_updatable_software()
        if message.lower() == "software":
            return SystemFunctions.get_all_software()
        if message.lower() == "upgrade":
            return SystemFunctions.update_all_software()

        split_message = message.split()
        if len(split_message) == 2:
            if split_message[0].lower() == "install":
                return SystemFunctions.install_program(split_message[1])
            if split_message[0].lower() == "uninstall":
                return SystemFunctions.uninstall_program(split_message[1])
            if split_message[0].lower() == "upgrade":
                return SystemFunctions.update_software(split_message[1])

    def cleanup(self):
        print("[CLEANUP] Sending termination message")
        self.client.close()


if __name__ == "__main__":
    client = Client()
    client.run()