import pygame

'''
Each instance of this class represents a group of platforms and clouds. This is a single level.
'''
class Level(object):

    def __init__(self, screen):
        super(Level, self).__init__()
        self.level_group = pygame.sprite.Group()
        self.ending_group = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.screen = screen

        self.least_x = 0
        self.greatest_x = 0
        self.least_y = 0
        self.greatest_y = 0

    def add_platform(self, platform):
        self.level_group.add(platform)

    def set_ending(self, ending):
        self.ending = ending
        self.ending_group.add(ending)
        return ending

    # Calculate constraints
    def calc_max_values(self):
        for platform_sprite in self.level_group:
            if platform_sprite.rect.left < self.least_x:
                self.least_x = platform_sprite.rect.left
            if platform_sprite.rect.right > self.greatest_x:
                self.greatest_x = platform_sprite.rect.right
            if platform_sprite.rect.top < self.least_y:
                self.least_y = platform_sprite.rect.top
            if platform_sprite.rect.bottom > self.greatest_y:
                self.greatest_y = platform_sprite.rect.bottom
        if self.ending.rect.right > self.greatest_x:
            self.greatest_x = self.ending.rect.right
        if self.ending.rect.left < self.least_x:
            self.least_x = self.ending.rect.left
        if self.ending.rect.bottom > self.greatest_y:
            self.greatest_y = self.ending.rect.bottom
        if self.ending.rect.top < self.least_y:
            self.least_y = self.ending.rect.top
        self.greatest_x += 150
        self.least_x -= 150
        self.greatest_y += 450
        self.least_y -= 450

    def update(self):
        self.enemy_count = len(self.enemies)
        if self.enemy_count <= 0:
            self.ending.unlock()

    def draw(self):
        self.level_group.draw(self.screen)
        self.ending_group.draw(self.screen)
        self.enemies.draw(self.screen)
