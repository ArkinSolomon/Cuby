from level import Level
from game_platform import Platform
from ending import Ending
from enemy import Enemy
from movable_object import Movable_Object
import pygame

'''
This file contains all of the game levels.
'''

# Colors
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
GREEN = pygame.Color('green')
BLUE = pygame.Color('blue')
PURPLE = pygame.Color('purple')

# Level 1
class Level1(Level):
    def __init__(self, screen):
        super(Level1, self).__init__(screen)

        # Make the level
        self.player_start = [100, 300]
        self.add_platform(Platform([0, 500], 700, 25, BLACK, screen))
        self.add_platform(Platform([500, 200], 100, 325, BLACK, screen))
        self.add_platform(Platform([700, 500], 100, 125, BLACK, screen))
        self.add_platform(Platform([800, 600], 500, 25, BLACK, screen))
        self.add_platform(Platform([1300, 500], 500, 25, BLACK, screen))
        self.add_platform(Platform([1900, 400], 300, 25, BLACK, screen))
        self.add_platform(Platform([1820, 200], 100, 25, BLACK, screen))
        self.add_platform(Platform([1800, -100], 400, 25, BLACK, screen))
        self.add_platform(Platform([1300, 0], 300, 25, BLACK, screen))
        self.ending = self.set_ending(Ending([2000, -300], screen))
        self.calc_max_values()

        # Add objects
        self.add_object(Movable_Object([200, 100]))

        # Add enemies
        self.enemies.add(Enemy([900, 300], screen))
        self.enemies.add(Enemy([800, 300], screen))

# Level 2
class Level2(Level):
    def __init__(self, screen):
        super(Level2, self).__init__(screen)

        # Start making the level
        self.player_start = [100, 300]
        self.add_platform(Platform([0, 500], 700, 25, BLUE, screen))
        self.add_platform(Platform([600, 400], 100, 100, BLUE, screen))
        self.add_platform(Platform([800, 600], 500, 25, BLUE, screen))
        self.add_platform(Platform([1300, 500], 500, 25, BLUE, screen))
        self.ending = self.set_ending(Ending([2000, 300], screen))
        self.calc_max_values()

# Level 3
class Level3(Level):
    def __init__(self, screen):
        super(Level3, self).__init__(screen)

        self.player_start = [100, 350]
        self.add_platform(Platform([0, 700], 5000, 25, BLACK, screen))
        self.ending = self.set_ending(Ending([5000, 500], screen))
        self.calc_max_values()

# Level 4
class Level4(Level):
    def __init__(self, screen):
        super(Level4, self).__init__(screen)

        platform_x = 100
        platform_y = 500

        self.player_start = [100, 300]
        for _ in range(20):
            self.add_platform(Platform([platform_x, platform_y], 300, 25, PURPLE, screen))
            platform_x += 300
            platform_y -= 200
        self.ending = self.set_ending(Ending([platform_x, platform_y], screen))
        self.calc_max_values()
