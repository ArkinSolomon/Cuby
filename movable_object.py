import pygame

class Movable_Object(pygame.sprite.Sprite):

    def __init__(self, starting_position):
        super(Movable_Object, self).__init__()

        self.pos = starting_position
        self.vertical_acceleration = 0
        self.prev_x = starting_position[0]
        self.prev_y = starting_position[1]
        self.delta = 0

        # Initialize sprite
        self.image = pygame.Surface((100, 100))
        self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.prev_x = self.pos[0]
        self.rect.y = self.pos[1]
        self.prev_y = self.pos[1]
