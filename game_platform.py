import pygame

'''
This class creates a platform.
'''
class Platform(pygame.sprite.Sprite):

    def __init__(self, position, width, height, color, screen):
        super(Platform, self).__init__()

        # Initialize variables
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.screen = screen
        self.drawn = False

        # Initialize platform
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        pygame.draw.rect(self.screen, self.color, [position[0], position[1], self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
