import socket
import threading
import struct
import time
import serverSender
import pickle
import Bullet
import Tower
import Bot

class ServerBulletSender(threading.Thread):
    def __init__(self, game, mySocket, clientsList):
        self.mySocket = mySocket
        threading.Thread.__init__(self)
        self.game = game
        self.clientList = clientsList


    def run(self):
        toSend = True
        while True:
            time.sleep(0.10)
            if self.game.shouldSend is True:
                for clients in self.clientList:
                    toSend = False
                    clients.send(pickle.dumps(self.game.sbulletList))
                self.game.shouldSend = False