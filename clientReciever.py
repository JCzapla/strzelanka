import threading
import struct
import time
import pickle
import Bullet
import Tower
import Bot

class ClientReciever(threading.Thread):
    def __init__(self, game, mySocket):
        self.mySocket = mySocket
        threading.Thread.__init__(self)
        self.game = game

    def run(self):
        while True:
            time.sleep(0.07)
            data = self.mySocket.recv(32768)
            try:
                data = pickle.loads(data)
            except:
                print("pickle sie wysral")
                data = None
                continue
            for towers in data:
                if isinstance(towers, Tower.Tower) or isinstance(towers, Bot.Bot):
                    if towers.position != self.game.player.position:
                        for bots in self.game.botList.sprites():
                            if bots.position == towers.position:
                                bots.setX(towers.rect.x)
                                bots.setY(towers.rect.y)
                else:
                    for bullets in data:
                        for bots in self.game.botList:
                            if bullets.position == bots.position:
                                newBullet = Bullet.Bullet(bullets.dx,bullets.dy,bullets.position)
                                self.game.sbulletList.add(newBullet)
                                bots.hasBullet = True
                                #self.game.shouldSend = True
                        for bullets2 in self.game.sbulletList:
                            bullets.load_image(bullets)
                            if bullets.position == bullets2.position:
                                bullets2.setX(bullets.rect.x)
                                bullets2.setY(bullets.rect.y)
