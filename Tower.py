import pygame
from Bullet import Bullet



class Tower(pygame.sprite.Sprite):

    def __init__(self,position,width):
        pygame.sprite.Sprite.__init__(self)



        self.width = 80
        self.height=35
        self.bullet_speed = 30
        self.hasBullet = False
        self.isDestroyed = False





        if position == 0:
            self.image = pygame.image.load('Sprites/tower.png')
            self.rect = self.image.get_rect()
            self.rect.x = width/2
            self.rect.y = width-self.height
            self.verticalAxis = 0
        elif position == 1:
            self.image = pygame.image.load('Sprites/Tower2.png')
            self.rect = self.image.get_rect()
            self.rect.x = width/2
            self.rect.y = 0
            self.verticalAxis=0
        elif position == 2:
            self.image = pygame.image.load('Sprites/tower3.png')
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = width/2
            self.verticalAxis=1
        elif position == 3:
            self.image = pygame.image.load('Sprites/tower4.png')
            self.rect = self.image.get_rect()
            self.rect.x = width-self.height
            self.rect.y = width/2
            self.verticalAxis = 1

        self.boundaryL = 40
        self.boundaryR = width - 40
        self.moving = 0
        self.position=position
        self.HP=3
        self.shotDirection=1

    def destroyed(self, gameDisplay):
            self.isDestroyed = True
            if self.position is 0:
                    self.image = pygame.image.load('Sprites/towerd.png')
                    gameDisplay.blit(self.image, (self.rect.x, self.rect.y))
            elif self.position is 1:
                    self.image = pygame.image.load('Sprites/Tower2d.png')
                    gameDisplay.blit(self.image, (self.rect.x, self.rect.y))
            elif self.position is 2:
                    self.image = pygame.image.load('Sprites/tower3d.png')
                    gameDisplay.blit(self.image, (self.rect.x, self.rect.y))
            elif self.position is 3:
                    self.image = pygame.image.load('Sprites/tower4d.png')
                    gameDisplay.blit(self.image, (self.rect.x, self.rect.y))


    def setMove(self,speed):
        self.moving=speed

    def hit(self):
        self.HP-=1
        return self.HP

    def setX(self,x):
        self.rect.x = x

    def setY(self,y):
        self.rect.y = y


    def move(self,gameDisplay):
        if self.verticalAxis==0:
            if not (self.rect.x + self.moving) < self.boundaryL:
                if not (self.rect.x + self.moving + self.width) > self.boundaryR:
                    self.rect.x += self.moving
        else:
            if not (self.rect.y + self.moving) < self.boundaryL:
                if not (self.rect.y + self.moving + self.width) > self.boundaryR:
                    self.rect.y += self.moving

        gameDisplay.blit(self.image,(self.rect.x,self.rect.y))

    def setShotDirection(self,value):
        self.shotDirection=value
    def shot(self):
        if self.position==0:
            if self.shotDirection == 0:
                bullet = Bullet(-self.bullet_speed, -self.bullet_speed,0)
                bullet.rect.x = self.rect.x + 6
                bullet.rect.y = self.rect.y
            elif self.shotDirection == 1:
                bullet = Bullet(0, -self.bullet_speed,0)
                bullet.rect.x = self.rect.x + 36  # +40 zeby na srodku wiezy
                bullet.rect.y = self.rect.y
            else:
                bullet = Bullet(self.bullet_speed, -self.bullet_speed,0)
                bullet.rect.x = self.rect.x + 74
                bullet.rect.y = self.rect.y


        elif self.position == 1:
            if self.shotDirection == 0:
                bullet = Bullet(self.bullet_speed, self.bullet_speed,1)
                bullet.rect.x = self.rect.x +74
                bullet.rect.y = self.rect.y +36
            elif self.shotDirection == 1:
                bullet = Bullet(0, self.bullet_speed,1)
                bullet.rect.x = self.rect.x + 36
                bullet.rect.y = self.rect.y+36
            else:
                bullet = Bullet(-self.bullet_speed, +self.bullet_speed,1)
                bullet.rect.x = self.rect.x + 6
                bullet.rect.y = self.rect.y+36

        elif self.position==2:
            if self.shotDirection == 0:
                bullet = Bullet(self.bullet_speed, -self.bullet_speed,2)
                bullet.rect.x = self.rect.x +37
                bullet.rect.y = self.rect.y +2
            elif self.shotDirection == 1:
                bullet = Bullet(self.bullet_speed, 0,2)
                bullet.rect.x = self.rect.x + 37
                bullet.rect.y = self.rect.y +36
            else:
                bullet = Bullet(self.bullet_speed, self.bullet_speed,2)
                bullet.rect.x = self.rect.x + 37
                bullet.rect.y = self.rect.y + 74

        elif self.position==3:
            if self.shotDirection == 0:
                bullet = Bullet(-self.bullet_speed, self.bullet_speed,3)
                bullet.rect.x = self.rect.x-100
                bullet.rect.y = self.rect.y +74
            elif self.shotDirection == 1:
                bullet = Bullet(-self.bullet_speed, 0,3)
                bullet.rect.x = self.rect.x -2
                bullet.rect.y = self.rect.y
            else:
                bullet = Bullet(-self.bullet_speed, -self.bullet_speed,3)
                bullet.rect.x = self.rect.x-2
                bullet.rect.y = self.rect.y + 6

        return bullet