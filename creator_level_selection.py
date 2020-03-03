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

        self.font = pygame.font.SysFont('Comic Sans MS', 25)
        self.fps_font = pygame.font.Font('fonts/FreeSansBold.ttf', 20)

        # Generate buttons
        columns = math.floor(screen_x / 120) - 1
        rows = math.floor((screen_y - 200) / 120)
        x_left = (screen_x - ((columns * 120) - 30)) / 2
        y_top = ((screen_y - 200) - ((rows * 120) - 30)) / 2
        count = 0
        for i in range(int(math.floor(len(levels) / (columns * rows)) + 1)):
            if self.VERBOSE: print 'Generating page %s' % str(i)
            page = pygame.sprite.Group()
            x = x_left
            y = y_top
            for _ in range(int(rows)):
                for _ in range(int(columns)):
                    count += 1
                    if self.VERBOSE: print 'Generating selection button for level %s' % str(count)
                    if count == len(levels) + 1:
                        page.add(Button([x, y], 90, 90, 'New', 36, screen))
                        break
                    else: page.add(Button([x, y], 90, 90, str(count), 50, screen))
                    if self.VERBOSE: print 'Generated selection button for level %s' % str(count)
                    x += 120
                if count == len(levels) + 1: break
                y += 120
                x = x_left
            if self.VERBOSE: print 'Generated page %s' % str(i)
            self.pages.append(page)

        self.back_button = Button([(screen_x / 2) - 190, screen_y - 145], 90, 90, 'Prev', 30, screen)
        self.next_button = Button([(screen_x / 2) + 100, screen_y - 145], 90, 90, 'Next', 30, screen)

        i = 0
        s = ''
        while i < len(str(len(self.pages))):
            s += '0'
            i += 1
        self.text_size = self.font.size('%s/%s' % (s, str(len(self.pages))))
        self.text = self.font.render('%s/%s' % (str(self.selected_page + 1), len(self.pages)), True, (0, 0, 0))
        self.text_coords = ((screen_x / 2) - (self.text_size[0] / 2), (screen_y - 100) - (self.text_size[1] / 2))

    def start(self):
        self.creator_level_selection_screen_is_active = True

        if len(self.pages) == 1:
            self.back_button.disabled = True
            self.next_button.disabled = True
        elif len(self.pages) > 1: self.back_button.disabled = True

        clock = pygame.time.Clock()

        if self.VERBOSE: print 'Level selection screen initialized'

        while self.creator_level_selection_screen_is_active:

            # Handle events
            for event in pygame.event.get():

                # If user quits
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    if self.VERBOSE: print 'Level selection canceled, returning to main menu'
                    return

            mouse_pos = pygame.mouse.get_pos()

            if self.back_button.check_click(mouse_pos[0], mouse_pos[1]):
                if self.VERBOSE: print 'Switching to level selection page %s' % str(self.selected_page)
                self.selected_page -= 1
                if self.selected_page == 0: self.back_button.disabled = True
                self.next_button.disabled = False
                self.text = self.font.render('%s/%s' % (str(self.selected_page + 1), len(self.pages)), True, (0, 0, 0))

            if self.next_button.check_click(mouse_pos[0], mouse_pos[1]):
                if self.VERBOSE: print 'Switching to level selection page %s' % str(self.selected_page + 2)
                self.selected_page += 1
                if self.selected_page == len(self.pages) - 1: self.next_button.disabled = True
                self.back_button.disabled = False
                self.text = self.font.render('%s/%s' % (str(self.selected_page + 1), len(self.pages)), True, (0, 0, 0))

            button = self.getClickedButton(mouse_pos)
            if button is not None:
                if button.text == 'New':
                    if self.VERBOSE: print 'Creating new level'
                    return Level_Creator(self.VERBOSE, self.SHOW_FPS).start(self.screen, None, None)
                else:
                    if self.VERBOSE: print 'Editing level %s' % button.text
                    selected_level = int(button.text) - 1
                    return Level_Creator(self.VERBOSE, self.SHOW_FPS).start(self.screen, self.levels[selected_level], selected_level)

            '''
            All drawing
            '''

            self.screen.fill(pygame.Color('lightblue'))
            self.screen.blit(self.SUN, (50, 50))

            for p in self.pages[self.selected_page]:
                p.draw()

            self.back_button.draw()
            self.next_button.draw()
            self.screen.blit(self.text, self.text_coords)

            if self.SHOW_FPS: self.screen.blit(self.fps_font.render(str(int(clock.get_fps())), True, pygame.Color('white'), pygame.Color('black')), (0, 0))

            pygame.display.flip()

            clock.tick(60)

    # Returns clicked button
    def getClickedButton(self, mouse_pos):
        for b in self.pages[self.selected_page]:
            if b.check_click(mouse_pos[0], mouse_pos[1]): return b
        return None
