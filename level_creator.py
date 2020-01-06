import pygame
import sys
from creation_type import Creation_Type
from game_platform import Platform
from movable_object import Movable_Object
from pathlib import Path
from enemy import Enemy
from button import Button

class Level_Creator(object):

    def __init__(self, verbose):
        super(Level_Creator, self).__init__()
        self.VERBOSE = verbose

        self.ON_KEY_PRESS_CHANGE_BY_VALUE = 10

        self.screen_x, self.screen_y = pygame.display.get_surface().get_size()
        self.offset = [0, 0]
        self.level_creator_is_active = True
        self.is_checking_for_mouse_up_event = False
        self.prevent_dual_click = False
        self.initial_mouse_pos = None
        self.final_mouse_pos = None
        self.type = Creation_Type.PLATFORM

        self.player_start = None
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.ending = None

    def start(self, screen):

        clock = pygame.time.Clock()
        button_y = self.screen_y - 90
        BUTTON_SIZE = 90
        BUTTON_X_DELTA = 45
        button_x = 90

        self.set_player_start_button = Button([button_x, button_y], BUTTON_SIZE, BUTTON_SIZE, 'Player', 30, screen)
        button_x += BUTTON_X_DELTA + BUTTON_SIZE
        self.set_platform_button = Button([button_x, button_y], BUTTON_SIZE, BUTTON_SIZE, 'Platform', 20, screen)
        button_x += BUTTON_X_DELTA + BUTTON_SIZE
        self.set_enemy_button = Button([button_x, button_y], BUTTON_SIZE, BUTTON_SIZE, 'Enemy', 30, screen)
        button_x += BUTTON_X_DELTA + BUTTON_SIZE
        self.set_ending_button = Button([button_x, button_y], BUTTON_SIZE, BUTTON_SIZE, 'Ending', 30, screen)
        button_x += BUTTON_X_DELTA + BUTTON_SIZE
        self.set_object_button = Button([button_x, button_y], BUTTON_SIZE, BUTTON_SIZE, 'Object', 25, screen)

        self.save_button = Button([self.screen_x - 360, button_y], BUTTON_SIZE, BUTTON_SIZE, 'Save', 30, screen)
        self.cancel_buttton = Button([self.screen_x - 180, button_y], BUTTON_SIZE, BUTTON_SIZE, 'Cancel', 30, screen)

        while self.level_creator_is_active:

            mouse_pos = pygame.mouse.get_pos()
            button_clicks = self.__calculate_button_clicks(mouse_pos)
            all_sprites = self.sprites.copy()
            all_sprites.add(self.enemies)
            all_sprites.add(self.objects)

            # Handle events
            for event in pygame.event.get():

                # If user quits
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.stop()

                # Mouse movements
                if event.type == pygame.MOUSEBUTTONDOWN and not self.is_checking_for_mouse_up_event:
                    mouse_pos = pygame.mouse.get_pos()
                    button_clicks = self.__calculate_button_clicks(mouse_pos)
                    if self.type == Creation_Type.PLATFORM:
                        self.is_checking_for_mouse_up_event = True
                        self.initial_mouse_pos = pygame.mouse.get_pos()
                    elif not self.prevent_dual_click and True not in button_clicks:
                        self.prevent_dual_click = True
                        if self.type == Creation_Type.PLAYER:
                            self.player_start = [mouse_pos[0] + self.offset[0], mouse_pos[1] + self.offset[1]]
                        elif self.type == Creation_Type.ENEMY:
                            self.enemies.add(Enemy([mouse_pos[0] + self.offset[0], mouse_pos[1] + self.offset[1]], screen))
                        elif self.type == Creation_Type.ENDING:
                            self.ending = [mouse_pos[0] + self.offset[0], mouse_pos[1] + self.offset[1]]
                        elif self.type == Creation_Type.OBJECT:
                            self.objects.add(Movable_Object([mouse_pos[0] + self.offset[0], mouse_pos[1] + self.offset[1]]))
                if event.type == pygame.MOUSEBUTTONUP and (self.is_checking_for_mouse_up_event or self.prevent_dual_click):
                    if self.prevent_dual_click:
                        self.prevent_dual_click = False
                    elif self.is_checking_for_mouse_up_event:
                        self.is_checking_for_mouse_up_event = False
                        self.final_mouse_pos = pygame.mouse.get_pos()
                        if self.final_mouse_pos != self.initial_mouse_pos and self.final_mouse_pos[0] != self.initial_mouse_pos[0] and self.final_mouse_pos[1] != self.initial_mouse_pos[1]:

                            top_left = self.__calculate_top_left(self.final_mouse_pos)

                            w = abs(self.final_mouse_pos[0] - self.initial_mouse_pos[0])
                            h = abs(self.final_mouse_pos[1] - self.initial_mouse_pos[1])

                            top_left[0] += self.offset[0]
                            top_left[1] += self.offset[1]

                            self.sprites.add(Platform(top_left, w, h, pygame.Color('black'), screen))

            # Screen movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.offset[1] -= self.ON_KEY_PRESS_CHANGE_BY_VALUE
            if keys[pygame.K_a]:
                self.offset[0] -= self.ON_KEY_PRESS_CHANGE_BY_VALUE
            if keys[pygame.K_s]:
                self.offset[1] += self.ON_KEY_PRESS_CHANGE_BY_VALUE
            if keys[pygame.K_d]:
                self.offset[0] += self.ON_KEY_PRESS_CHANGE_BY_VALUE

            # Delete sprites
            if keys[pygame.K_DELETE] or keys[pygame.K_BACKSPACE]:
                for sprite in all_sprites:
                    if sprite.rect.collidepoint((mouse_pos[0] + self.offset[0], mouse_pos[1] + self.offset[1])):
                        sprite.kill()

            # Reset camera
            if keys[pygame.K_SPACE]:
                self.offset = [0, 0]

            # Change placement types
            if button_clicks[0]:
                self.type = Creation_Type.PLAYER
            if button_clicks[1]:
                self.type = Creation_Type.PLATFORM
            if button_clicks[2]:
                self.type = Creation_Type.ENEMY
            if button_clicks[3]:
                self.type = Creation_Type.ENDING
            if button_clicks[4]:
                self.type = Creation_Type.OBJECT

            # Save the file
            if button_clicks[5]:
                level_path = Path('%s/%s' % ('levels', 'levels.lvl'))
                with level_path.open(mode='a+') as file:
                    file.write(u'*LEVEL*\n')
                    file.write(u'PLS$[%d,%d]\n' % (self.player_start[0], self.player_start[1]))
                    for platform in self.sprites: file.write(u'PLA$[%d,%d]$%d$%d$#000000\n' % (platform.position[0], platform.position[1], platform.width, platform.height))
                    for enemy in self.enemies: file.write(u'ENE$[%d,%d]\n' % (enemy.pos[0], enemy.pos[1]))
                    for object in self.objects: file.write(u'OBJ$[%d,%d]\n' % (object.pos[0], object.pos[1]))
                    file.write(u'END$[%d,%d]\n' % (self.ending[0], self.ending[1]))
                self.level_creator_is_active = False
                return

            # Draw sky
            screen.fill(pygame.Color('lightblue'))
            screen.blit(pygame.image.load('sun.png'), (50, 50))

            # Draw and offset platforms
            for sprite in all_sprites:
                sprite.rect.x -= self.offset[0]
                sprite.rect.y -= self.offset[1]

            all_sprites.draw(screen)

            if len(all_sprites) == 0:
                self.cancel_buttton.disabled = True
            else:
                self.cancel_button.disabled = False

            for sprite in all_sprites:
                sprite.rect.x += self.offset[0]
                sprite.rect.y += self.offset[1]

            if self.player_start != None:
                s = pygame.Surface((150, 150))
                s.blit(pygame.image.load('player.png'), s.get_rect())
                screen.blit(s, [self.player_start[0] - self.offset[0], self.player_start[1] - self.offset[1]])

            if self.ending != None:
                s = pygame.Surface((200, 200))
                s.fill(pygame.Color('green'))
                screen.blit(s, [self.ending[0] - self.offset[0], self.ending[1] - self.offset[1]])

            # Draw preview
            if self.type == Creation_Type.PLAYER:
                s = pygame.Surface((150, 150))
                s.set_alpha(128)
                s.blit(pygame.image.load('player.png'), s.get_rect())
                screen.blit(s, mouse_pos)
            elif self.is_checking_for_mouse_up_event and self.type == Creation_Type.PLATFORM:

                top_left = self.__calculate_top_left(mouse_pos)

                w = abs(mouse_pos[0] - self.initial_mouse_pos[0])
                h = abs(mouse_pos[1] - self.initial_mouse_pos[1])

                s = pygame.Surface((w, h))
                s.set_alpha(128)
                s.fill(pygame.Color('black'))
                screen.blit(s, top_left)
            elif self.type == Creation_Type.ENEMY:
                s = pygame.Surface((75, 75), pygame.SRCALPHA)
                s.set_alpha(128)
                s.blit(pygame.image.load('enemy.png'), s.get_rect())
                screen.blit(s, mouse_pos)
            elif self.type == Creation_Type.ENDING:
                s = pygame.Surface((200, 200))
                s.set_alpha(128)
                s.fill(pygame.Color('green'))
                screen.blit(s, mouse_pos)
            elif self.type == Creation_Type.OBJECT:
                s = pygame.Surface((100, 100))
                s.set_alpha(128)
                s.fill(pygame.Color('red'))
                screen.blit(s, mouse_pos)

            self.set_player_start_button.draw()
            self.set_platform_button.draw()
            self.set_enemy_button.draw()
            self.set_ending_button.draw()
            self.set_object_button.draw()
            self.save_button.draw()
            self.cancel_buttton.draw()

            pygame.display.flip()
            clock.tick(800)

    def __calculate_top_left(self, pos):
        top_left = [0, 0]
        if self.initial_mouse_pos[0] < pos[0]:
            top_left[0] = self.initial_mouse_pos[0]
        else:
            top_left[0] = pos[0]
        if self.initial_mouse_pos[1] < pos[1]:
            top_left[1] = self.initial_mouse_pos[1]
        else:
            top_left[1] = pos[1]
        return top_left

    def __calculate_button_clicks(self, mouse_pos):
        return [self.set_player_start_button.check_click(mouse_pos[0], mouse_pos[1]), self.set_platform_button.check_click(mouse_pos[0], mouse_pos[1]), self.set_enemy_button.check_click(mouse_pos[0], mouse_pos[1]), self.set_ending_button.check_click(mouse_pos[0], mouse_pos[1]), self.set_object_button.check_click(mouse_pos[0], mouse_pos[1]), self.save_button.check_click(mouse_pos[0], mouse_pos[1])]

    def stop(self):
        if self.VERBOSE: print 'Halt signal recieved, creator closing'
        self.level_creator_is_active = False
        pygame.quit()
        sys.exit(0)
