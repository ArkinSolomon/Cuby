import pygame
from level_creator import Level_Creator

class Creator_Level_Selection:

    def __init__(self, levels, screen, screen_x, screen_y):
        self.levels = levels
        self.screen = screen
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.creator_level_selection_screen_is_active = False

    def start(self):
        self.creator_level_selection_screen_is_active = True
