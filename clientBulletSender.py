import socket
import threading
import struct
import time
import pickle
import pygame
import copy

class ClientBulletSender(threading.Thread):
    def __init__(self, game, mySocket):

        """
        self.mySocket = socket.socket()
        threading.Thread.__init__(self)
        host = socket.gethostname()
        port = 12345
        self.mySocket.connect((host, port))
        self.game = game
        """

        self.mySocket = mySocket
        threading.Thread.__init__(self)
        self.game = game




    def run(self):
        while True:
                time.sleep(0.15)
                while self.game.shouldSend is True:
                    self.mySocket.send(pickle.dumps(self.game.sbulletList))
                    self.game.shouldSend = False