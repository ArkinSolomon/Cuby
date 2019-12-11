import pygame
from random import randrange
from cloud_part import Cloud_Part

'''
This class creates clouds at random locations in the screen.
'''
class Cloud(object):

    # Class initializer
    def __init__(self, screen, width, height):
        super(Cloud, self).__init__()
        self.clouds = pygame.sprite.Group()
        self.part_size = 40

        # All possible clouds
        POSSIBLE_CLOUDS = [30, 15, 39, 38, 57, 60, 58, 23]

        # Print a random amount of clouds
        for i in range(randrange(5, 10, 1)):
            current_cloud = list(bin(POSSIBLE_CLOUDS[randrange(0, len(POSSIBLE_CLOUDS) - 1, 1)])[2:])

            # Make sure cloud has 6 parts
            if len(current_cloud) < 6:
                for j in range(6 - len(current_cloud)):
                    current_cloud.insert(0, 0)

            x = randrange(0, width - (self.part_size * 3), self.part_size)
            y = randrange(0, height - (self.part_size * 3), self.part_size)
            y_inc_count = 0

            # Create cloud
            for cloud_part in current_cloud:
                if cloud_part == '1':
                    self.clouds.add(Cloud_Part(screen, x, y, self.part_size))
                x += self.part_size
                y_inc_count += 1
                if y_inc_count == 3:
                    y += self.part_size
                    x -= self.part_size * 3
