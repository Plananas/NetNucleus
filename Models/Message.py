import socket

class Message(object):
    FORMAT = 'utf-8'
    HEADER = 64

    def __init__(self, _conn):
        self.conn = _conn

    # Read the message sent from the client.
    def read(self):
        messages = []
        msg_length = self.conn.recv(self.HEADER).decode(self.FORMAT)
        msg_length = int(msg_length)
        if msg_length:
            messages.append(self.conn.recv(msg_length))
        # This will be the final decoded message!
        try:
            message = messages[0].decode('utf-8')

            return str(message)
        except:
            return("Error Decoding Message")

    # write a message to the client.
    def write(self, message):

        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.conn.send(send_length)
        self.conn.send(message)
