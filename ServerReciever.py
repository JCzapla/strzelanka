import threading
import time
import pickle
import Tower
import Bullet
import Bot


class ServerReciever(threading.Thread):
    def __init__(self, game, mySocket, clientsList):
        self.mySocket = mySocket
        threading.Thread.__init__(self)
        self.game = game
        self.clientList = clientsList


    def run(self):
        while True:
                time.sleep(0.05)
                # data2 = clients.recv(8192)
                data = self.clientList[1].recv(1024)
                data = pickle.loads(data)
                for towers in data:
                    if isinstance(towers, Tower.Tower) or isinstance(towers, Bot.Bot):
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
