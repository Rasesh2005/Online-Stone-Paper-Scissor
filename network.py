import socket
import pickle

class Network:
    def __init__(self):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.IP=socket.gethostbyname(socket.gethostname())
        self.PORT=1234
        self.ADDR=(self.IP,self.PORT)
        self.FORMAT="utf-8"
        self.pos=self.connect()
    def get_pos(self):
        return self.pos
    def connect(self):
        try:
            self.client.connect(self.ADDR)
            return self.client.recv(2048).decode(self.FORMAT)
        except:
            pass

    def send(self,data):
        try:
            self.client.send(data.encode(self.FORMAT))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print("[SOCKET ERROR]",e)

