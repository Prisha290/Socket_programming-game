class SocketWrapper(object):

    def __init__(self, socket):
        self.socket = socket

    def recv_data(self):

        try:
            return self.socket.recv(512).decode('utf-8')
        except:
            return ""

    def send_data(self, message):
        return self.socket.send(message.encode('utf-8'))

    def close(self):
        self.socket.close()
