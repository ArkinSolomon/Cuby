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
        self.objects = pygame.sprite.Group()
        self.screen = screen
        self.render = True

        self.screen_x, self.screen_y = pygame.display.get_surface().get_size()

        self.least_x = 0
        self.greatest_x = 0
        self.least_y = 0
        self.greatest_y = 0

    def add_platform(self, platform):
        self.level_group.add(platform)

    def add_object(self, object):
        self.objects.add(object)

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

    def set_clouds(self, cloud_group):
        self.clouds = cloud_group

    def stop_render(self):
        self.render = False

    def start_render(self):
        self.render = True

    def __check_draw(self, sprite_group):
        for sprite in sprite_group:
            if self.render:
                if (sprite.rect.right >= 0 and sprite.rect.right <= self.screen_x) or (sprite.rect.left >= 0 and sprite.rect.left <= self.screen_x) or (sprite.rect.top >= 0 and sprite.rect.top <= self.screen_y) or (sprite.rect.bottom >= 0 and sprite.rect.bottom <= self.screen_y):
                    self.screen.blit(sprite.image, sprite.rect)
                    sprite.drawn = True
                else:
                    sprite.drawn = False
            else:
                if sprite.drawn:
                    self.screen.blit(sprite.image, sprite.rect)

    def draw(self):
        self.__check_draw(self.clouds)
        self.__check_draw(self.level_group)
        self.__check_draw(self.ending_group)
        self.__check_draw(self.objects)
        self.__check_draw(self.enemies)
