
import socket
import threading
import struct
import time
import serverSender
import pickle
import Bullet
import Tower
import Bot
import sys

class Server(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        self.mySocket = socket.socket()
        host = socket.gethostname()
        port = 12345
        try:
            self.mySocket.bind(('', port))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
        self.clientList = []
        self.game = game
        self.data = []

    def run(self):
        while True:
                time.sleep(0.05)
                #data2 = clients.recv(8192)
                data = self.clientList[0].recv(8192)
                data = pickle.loads(data)
                for towers in data:
                    if isinstance(towers,Tower.Tower) or isinstance(towers,Bot.Bot):
                        if towers.position != self.game.player.position:
                            for bots in self.game.botList.sprites():
                                if bots.position == towers.position:
                                    bots.setX(towers.rect.x)
                                    bots.setY(towers.rect.y)
                    else:
                        for bullets in data:
                            if isinstance(bullets, Bullet.Bullet):
                                for bots in self.game.botList:
                                    if bullets.position == bots.position:
                                        newBullet = Bullet.Bullet(bullets.dx, bullets.dy, bullets.position)
                                        self.game.sbulletList.add(newBullet)
                                        bots.hasBullet = True
                                        self.game.shouldSend = True
                                for bullets2 in self.game.sbulletList:
                                    bullets.load_image(bullets)
                                    if bullets.position == bullets2.position:
                                        bullets2.setX(bullets.rect.x)
                                        bullets2.setY(bullets.rect.y)




    def Connection(self):
        self.mySocket.listen(5)
        c, addr = self.mySocket.accept()
        self.clientList.append(c)
        return len(self.clientList)