import socket
import threading
import time
import pickle

class Client(threading.Thread):
    def __init__(self, game,ipText):
        self.mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        threading.Thread.__init__(self)
        host = socket.gethostname()
        port = 12345
        self.mySocket.connect((ipText, port))
        self.game = game



    def run(self):
        while True:
            time.sleep(0.07)
            if self.game.shouldSend is True:
                continue
            else:
                self.mySocket.send(pickle.dumps(self.game.towerList))




