import pygame

'''
This class is the ending of a level.
'''
class Ending(pygame.sprite.Sprite):

    def __init__(self, coords, screen):
        super(Ending, self).__init__()

        # Initialize variables
        self.size = [200, 200]
        self.color = pygame.Color('red')
        self.locked = True
        self.screen = screen
        self.drawn = False

        # Initialize sprite
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        pygame.draw.rect(self.screen, self.color, [coords[0], coords[1], self.size[0], self.size[1]])
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def unlock(self):
        self.locked = False
        self.color = pygame.Color('green')
        self.image.fill(self.color)
        pygame.draw.rect(self.screen, self.color, [self.rect.x, self.rect.y, self.size[0], self.size[1]])
