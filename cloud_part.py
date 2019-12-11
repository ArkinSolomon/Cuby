import pygame

'''
This class represents where the edning is in a level.
'''
class Cloud_Part(pygame.sprite.Sprite):

    def __init__(self, screen, x, y, size):
        super(Cloud_Part, self).__init__()

        self.color = pygame.Color('white')

        self.image = pygame.Surface([size, size])
        self.image.fill(self.color)
        pygame.draw.rect(screen, self.color, [x, y, size, size])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
