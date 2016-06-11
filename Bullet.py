import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self,directionX,directionY,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Sprites/bullet.png')
        self.rect = self.image.get_rect()
        self.dy = directionY
        self.dx = directionX
        self.position = position


    def load_image(self, o):
        o.image = pygame.image.load('Sprites/bullet.png')

    def move(self, gameDisplay):
        self.rect.y += self.dy
        self.rect.x += self.dx
        gameDisplay.blit(self.image, (self.rect.x, self.rect.y))

    def setX(self, x):
        self.rect.x = x

    def setY(self, y):
        self.rect.y = y