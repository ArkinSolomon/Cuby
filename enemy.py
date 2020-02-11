import pygame

class Enemy(pygame.sprite.Sprite):

    def __init__(self, starting_position, screen):
        super(Enemy, self).__init__()

        self.pos = starting_position
        self.speed = 3.6
        self.vertical_acceleration = 0
        self.prev_x = starting_position[0]
        self.prev_y = starting_position[1]
        self.is_in_air = False
        self.jump_power = 8
        self.drawn = False
        self.is_enabled = True
        self.has_ai = True

        # Initialize sprite
        self.image = pygame.Surface((75, 75), pygame.SRCALPHA)
        self.image.blit(pygame.image.load('images/enemy.png'), self.image.get_rect())
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.prev_x = self.pos[0]
        self.rect.y = self.pos[1]
        self.prev_y = self.pos[1]

    def jump(self):
        if not self.is_in_air: self.vertical_acceleration -= self.jump_power

    def kill_by_player(self): self.is_enabled = False
