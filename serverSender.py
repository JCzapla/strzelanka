import threading
import time
import struct
import pickle
import pygame
import copy

class ServerSender(threading.Thread):
    def __init__(self, game, mySocket,clientsList):
        self.mySocket = mySocket
        threading.Thread.__init__(self)
        self.game = game
        self.clientList = clientsList

    def run(self):
        while True:
                for clients in self.clientList:
                    time.sleep(0.07)
                    clients.send(pickle.dumps(self.game.towerList))
