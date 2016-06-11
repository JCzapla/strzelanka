import pygame
import Tower
from Bot import Bot
from random import randint
import time
import Server
import Client
import struct
import serverSender
import clientReciever
import serverBulletSender
import clientBulletSender
import ServerReciever



class Game:
    def __init__(self):
        pygame.init()
        self.spritesList = pygame.sprite.Group()
        self.sbulletList = pygame.sprite.Group()
        self.towerList = pygame.sprite.Group()
        self.botList = pygame.sprite.Group()
        self.towerList2 = pygame.sprite.Group()
        self.screenWidth = 720
        self.screenHeight = 720
        self.gameDisplay = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.clock = pygame.time.Clock()
        pygame.display.update()
        self.black = (0,0,0)
        self.player=0
        self.players = 0
        self.blt = False
        self.myBullet = None
        self.shouldSend = False
        self.shouldSendTowers = False


def ipInsertion(ipText):
    while True:
        for event in pygame.event.get():
            print("jestem")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    return ipText
                ipText.append(event.key)


if __name__ == '__main__':
    game = Game()
    gameExit = False
    waitingToChoose = True
    waitingToConnect = True
    showMessage = True
    initializeConnection = True
    initializeBoard = True
    isBullet = False
    ipText = []
    ipToSend = []


    while not gameExit:

        while waitingToChoose:
            game.gameDisplay.fill(game.black)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        myServer = Server.Server(game)
                        print("Wybrales Hosta")
                        tower = Tower.Tower(0, game.screenWidth)
                        game.player = tower
                        game.spritesList.add(tower)
                        game.towerList.add(tower)
                        game.towerList2.add(tower)
                        isServer = True
                        isClient = False
                        waitingToChoose = False
                        break
                    if event.key == pygame.K_k:
                        print("Wybrales Kileinta")
                        ipText = ipInsertion(ipText)
                        for char in ipText:
                            a = chr(char)
                            ipToSend.append(a)
                        ip = ''.join(ipToSend)
                        myClient = Client.Client(game,ip)
                        playerPos = myClient.mySocket.recv(4)
                        playerPos = struct.unpack("I", playerPos)
                        tower = Tower.Tower(playerPos[0], game.screenWidth)
                        game.player = tower#25.144.15.28
                        game.spritesList.add(tower)
                        game.towerList.add(tower)
                        game.towerList2.add(tower)
                        isServer = False
                        isClient = True
                        waitingToChoose = False
                        break

        if isServer and initializeConnection:
            if showMessage:
                print("Waiting for clients to connect")
            while waitingToConnect:
                ilosc = myServer.Connection()
                for clients in myServer.clientList:
                    clients.send(struct.pack("I", ilosc))
                if ilosc == 2:
                    print("4 players ", ilosc)
                    waitingToConnect = False
                    showMessage = False
                    myServer.clientList[1].send(struct.pack("I", ilosc))
            initializeConnection = False

        if isClient:
            if showMessage:
                print("Waiting for clients to connect")
            while waitingToConnect:
                ilosc = myClient.mySocket.recv(4)
                ilosc = struct.unpack("I",ilosc)
                if ilosc[0] == 2:
                    print("4 players ", ilosc)
                    waitingToConnect = False
                    showMessage = False


        if isServer and initializeBoard :
            index = 1
            for clients in myServer.clientList:
                bot = Bot(index,game.screenWidth)
                game.botList.add(bot)
                game.towerList.add(bot)
                game.spritesList.add(bot)
                game.towerList2.add(bot)
                index += 1
            initializeBoard = False
            mySender = serverSender.ServerSender(game, myServer.mySocket,myServer.clientList)
            mySender2 = serverBulletSender.ServerBulletSender(game, myServer.mySocket, myServer.clientList)
            myReciever = ServerReciever.ServerReciever(game,myServer.mySocket,myServer.clientList)
            myServer.start()
            mySender.start()
            mySender2.start()
            myReciever.start()

        if isClient and initializeBoard:
            index = 0
            playersWhoConnected = 2
            while playersWhoConnected != 0:
                if game.player.position != index:
                    bot = Bot(index, game.screenWidth)
                    game.botList.add(bot)
                    game.spritesList.add(bot)
                    game.towerList2.add(bot)
                    index += 1
                    game.players += 1
                    playersWhoConnected -= 1
                else:
                    index += 1
            myReciever = clientReciever.ClientReciever(game,myClient.mySocket)
            myClientSender = clientBulletSender.ClientBulletSender(game,myClient.mySocket)
            myClient.start()
            myReciever.start()
            myClientSender.start()
            initializeBoard = False

        game.gameDisplay.fill(game.black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if game.player.isDestroyed is False:
                        game.player.setMove(-5)
                        game.shouldSendTowers = True
                if event.key == pygame.K_RIGHT:
                    if game.player.isDestroyed is False:
                        game.player.setMove(5)
                        game.shouldSendTowers = True
                if event.key == pygame.K_SPACE:
                    if game.player.isDestroyed is False:
                        if game.blt is False:
                            bullet = game.player.shot()
                            game.sbulletList.add(bullet)
                            game.blt = True
                            game.player.hasBullet = True
                            game.shouldSend = True
                if event.key==pygame.K_z:
                    game.player.setShotDirection(0)
                if event.key == pygame.K_x:
                    game.player.setShotDirection(1)
                if event.key == pygame.K_c:
                    game.player.setShotDirection(2)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    game.player.setMove(0)

        game.player.move(game.gameDisplay)
        game.botList.draw(game.gameDisplay)
        for bullets in game.sbulletList:
            bullets.load_image(bullets)
        game.sbulletList.draw(game.gameDisplay)
        for bullets in game.sbulletList.sprites():
            if bullets.rect.x > 720 or bullets.rect.x < 0 or  bullets.rect.y > 720 or  bullets.rect.y < 0:
                game.sbulletList.remove(bullets)
                for bots in game.botList:
                    if bots.position == bullets.position:
                        bots.hasBullet = False
                bullet = None
                if bullets.position == game.player.position:
                    game.blt = False
                    game.player.hasBullet = False
        for bullets in game.sbulletList.sprites():
            bullets.move(game.gameDisplay)

        for towers in game.towerList2.sprites():
            if pygame.sprite.spritecollide(towers, game.sbulletList,False):
                towers.isDestroyed = True

        for towers in game.towerList2.sprites():
            if towers.isDestroyed is True:
                towers.destroyed(game.gameDisplay)


        #for towers in game.botList.sprites():
         #   game.botList.draw(game.gameDisplay)
          #  if   pygame.sprite.spritecollide(towers, game.bulletList, True):
          #      hp = towers.hit()
            #
            #   if hp <= 0:
            #        game.botList.remove(towers)
              #      game.spritesList.remove(towers)


        #for bullets in game.bulletList.sprites():
          #  bullets.move(game.gameDisplay)
       # if pygame.sprite.spritecollide(game.player,game.bulletList, True):
        #    hp=game.player.hit()

        #    if hp<=0:
        #        print("przegrales")
        #        gameover=pygame.sprite.Sprite()
        #        gameover.image=pygame.image.load('Sprites/game_over.png')
         #       game.spritesList.add(gameover)
         #       pygame.display.update()
         #       time.sleep(4)
         #       pygame.quit()
         #       quit()
     #   cout=0
        #for x in game.botList:
         #   cout+=1
       # for x in game.towerList:
         #   cout+=1
        #if cout==1:
          #  print("WYGRALES")
           # time.sleep(4)
            #pygame.quit()
            #quit()



        pygame.display.update()
        game.clock.tick(60)

    pygame.quit()
    quit()

