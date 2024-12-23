import socket
import uuid

class MessageController(object):
    FORMAT = 'utf-8'
    HEADER = 64

    def __init__(self, connection):
        self.connection = connection
        self.messageId = str(uuid.uuid4())[:8]

    # Read the message sent from the client.
    def read(self):
        messageLength = self.connection.recv(self.HEADER).decode(self.FORMAT).strip()
        try:
            messageLength = int(messageLength)
        except ValueError:
            return "Invalid message length received"
        received_bytes = 0
        messageParts = []

        print(messageLength)

        while received_bytes < messageLength:
            part = self.connection.recv(min(messageLength - received_bytes, 1024))
            if not part:
                break
            messageParts.append(part)
            received_bytes += len(part)
        fullMessage = b''.join(messageParts)

        try:
            fullMessage = fullMessage.decode(self.FORMAT)
        except UnicodeDecodeError:
            return "Error Decoding Message"

        senderId, content = fullMessage.split(":", 1)
        # Ignore messages sent by this client
        if senderId != self.messageId:
            return content

    # write a message to the client.
    def write(self, message):
        fullMessage = f"{self.messageId}:{message}"

        messageLength = len(fullMessage.encode(self.FORMAT))
        sendLength = str(messageLength).encode(self.FORMAT)
        sendLength += b' ' * (self.HEADER - len(sendLength))
        self.connection.send(sendLength)
        self.connection.send(fullMessage.encode(self.FORMAT))

