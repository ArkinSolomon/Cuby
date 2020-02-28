import pygame
import math
from level_creator import Level_Creator
from button import Button

class Creator_Level_Selection:

    def __init__(self, levels, screen, screen_x, screen_y, VERBOSE, SHOW_FPS):
        self.levels = levels
        self.screen = screen
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.VERBOSE = VERBOSE
        self.SHOW_FPS = SHOW_FPS

        self.creator_level_selection_screen_is_active = False

        self.pages = []
        self.selected_page = 0

        self.SUN = pygame.image.load('images/sun.png')

        # Generate buttons
        columns = math.floor(screen_x / 120)
        rows = math.floor((screen_y - 200) / 120)
        x_left = (screen_x - rows * 120 - 30) / 2
        y_top = (screen_y - (((screen_y - 200) / 120) - 30)) / 2
        count = 0
        for _ in range(int(math.floor(len(levels) / (columns * rows)) + 1)):
            page = pygame.sprite.Group()
            x = x_left
            y = y_top
            for _ in range(int(rows)):
                for _ in range(int(columns)):
                    count += 1
                    page.add(Button([x, y], 90, 90, str(count), 50, screen))
                    x += 120
                y += 120
                x = x_left
            self.pages.append(page)

    def start(self):
        self.creator_level_selection_screen_is_active = True

        while self.creator_level_selection_screen_is_active:

            # Handle events
            for event in pygame.event.get():

                # If user quits
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    if self.VERBOSE: print 'Level selection canceled, returning to main menu'
                    return

            self.screen.fill(pygame.Color('lightblue'))
            self.screen.blit(self.SUN, (50, 50))

            for p in self.pages[self.selected_page]:
                p.draw()
            pygame.display.flip()
