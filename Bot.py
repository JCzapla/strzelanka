from Tower import Tower
from random import randint

class Bot(Tower):

    def __init__(self,position,width):
        Tower.__init__(self,position,width)
        self.direction = True
        self.movingSpeed=5

    def autoMove(self, gameDisplay):
        if self.verticalAxis ==0:
            if self.direction:
                if not (self.rect.x + self.movingSpeed + self.width) > self.boundaryR:
                    self.rect.x += self.movingSpeed
                else:
                    self.direction = False
            else:
                if not (self.rect.x - self.movingSpeed) < self.boundaryL:
                    self.rect.x -= self.movingSpeed
                else:
                    self.direction = True
        else:
            if self.direction:
                if not (self.rect.y + self.movingSpeed + self.width) > self.boundaryR:
                    self.rect.y += self.movingSpeed
                else:
                    self.direction = False
            else:
                if not (self.rect.y - self.movingSpeed) < self.boundaryL:
                    self.rect.y -= self.movingSpeed
                else:
                    self.direction = True
        gameDisplay.blit(self.image, (self.rect.x, self.rect.y))

    def shot(self):
        self.shotDirection=1
        return Tower.shot(self)