import pygame
from random import randrange
from cloud_part import Cloud_Part
import math

'''
This class creates clouds at random locations in the screen.
'''
class Cloud(object):

    # Class initializer
    def __init__(self, screen, width, height, horizontal_constraints, vertical_constraints, VERBOSE):
        super(Cloud, self).__init__()
        self.clouds = pygame.sprite.Group()
        self.part_size = 40

        # All possible clouds
        POSSIBLE_CLOUDS = [30, 15, 39, 38, 57, 60, 58, 23]

        # Print a random amount of clouds
        curr_x = horizontal_constraints[0]

        if VERBOSE: print('Creating cloud set')

        x_screens = int(math.ceil((horizontal_constraints[1] - horizontal_constraints[0]) / width))
        y_screens = int(math.ceil((vertical_constraints[1] - vertical_constraints[0]) / height))

        for _ in range(x_screens):
            curr_y = vertical_constraints[0]
            for _ in range(y_screens):
                for _ in range(randrange(8, 12, 1)):
                    CLOUD = POSSIBLE_CLOUDS[randrange(0, len(POSSIBLE_CLOUDS) - 1, 1)]
                    current_cloud = list(bin(CLOUD)[2:])

                    # Make sure cloud has 6 parts
                    if len(current_cloud) < 6:
                        for _ in range(6 - len(current_cloud)):
                            current_cloud.insert(0, 0)

                    x = randrange(curr_x, curr_x + (width - (self.part_size * 3)), self.part_size)
                    y = randrange(curr_y, curr_y + (height - (self.part_size * 3)), self.part_size)
                    y_inc_count = 0

                    if VERBOSE: print('Creating cloud at (%d, %d) [C#%d]') % (x, y, CLOUD)

                    # Create cloud
                    for cloud_part in current_cloud:
                        if cloud_part == '1':
                            self.clouds.add(Cloud_Part(screen, x, y, self.part_size))
                        x += self.part_size
                        y_inc_count += 1
                        if y_inc_count == 3:
                            y += self.part_size
                            x -= self.part_size * 3
                curr_y += height
            curr_x += width
