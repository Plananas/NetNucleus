import socket
import uuid

class Message(object):
    FORMAT = 'utf-8'
    HEADER = 64

    def __init__(self, connection):
        self.connection = connection
        self.messageId = str(uuid.uuid4())[:8]

    # Read the message sent from the client.
    def read(self):
        messages = []
        msg_length = self.connection.recv(self.HEADER).decode(self.FORMAT).strip()
        try:
            msg_length = int(msg_length)
        except ValueError:
            return "Invalid message length received"
        received_bytes = 0
        message_parts = []

        while received_bytes < msg_length:
            part = self.connection.recv(min(msg_length - received_bytes, 1024))
            if not part:
                break
            message_parts.append(part)
            received_bytes += len(part)
        fullMessage = b''.join(message_parts)

        try:
            fullMessage = fullMessage.decode(self.FORMAT)
        except UnicodeDecodeError:
            return "Error Decoding Message"

        sender_id, content = fullMessage.split(":", 1)
        # Ignore messages sent by this client
        if sender_id != self.messageId:
            return content

    # write a message to the client.
    def write(self, message):

        fullMessage = f"{self.messageId}:{message}"
        messageLength = len(fullMessage)
        sendLength = str(messageLength).encode(self.FORMAT)
        sendLength += b' ' * (self.HEADER - len(sendLength))
        self.connection.send(sendLength)
        self.connection.send(fullMessage.encode(self.FORMAT))

