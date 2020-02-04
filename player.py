import pygame

'''
This class holds player data. It's classed in order to build a base for multiplayer.
'''
class Player(pygame.sprite.Sprite):

    def __init__(self, starting_position, screen):
        super(Player, self).__init__()

        # Initialize variables
        self.score = 0
        self.pos = starting_position
        self.speed = 5
        self.vertical_acceleration = 0
        self.screen = screen
        self.color = pygame.Color('lightgreen')
        self.is_in_air = False
        self.health = 200
        self.is_slamming = False
        self.drawn = False
        self.direction = 'r'

        # Initialize player
        self.image = pygame.image.load('player.png')
        pygame.draw.rect(self.screen, self.color, [self.pos[0], self.pos[1], 150, 150], 0)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.prev_x = self.pos[0]
        self.rect.y = self.pos[1]
        self.prev_y = self.pos[1]
