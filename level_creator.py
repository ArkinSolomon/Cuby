import pygame
import sys
from creation_type import Creation_Type
from game_platform import Platform
from movable_object import Movable_Object
from pathlib import Path
from enemy import Enemy
from button import Button

class Level_Creator(object):

    def __init__(self, VERBOSE, SHOW_FPS):
        super(Level_Creator, self).__init__()
        self.VERBOSE = VERBOSE
        self.SHOW_FPS = SHOW_FPS

        self.ON_KEY_PRESS_CHANGE_BY_VALUE = 10

        self.screen_x, self.screen_y = pygame.display.get_surface().get_size()
        self.offset = [0, 0]
        self.level_creator_is_active = True
        self.is_checking_for_mouse_up_event = False
        self.prevent_dual_click = False
        self.initial_mouse_pos = None
        self.final_mouse_pos = None
        self.editing = False
        self.type = Creation_Type.PLATFORM
        self.FPS = 60
        self.delete = False

        self.player_start = None
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.ending = None

        # Load images
        self.ENEMY_IMAGE = pygame.image.load('images/enemy.png')
        self.PLAYER_IMAGE = pygame.image.load('images/player.png')
        self.SUN = pygame.image.load('images/sun.png')

        self.fps_font = pygame.font.Font('fonts/FreeSansBold.ttf', 20)

        if self.VERBOSE: print('Level Creator initialized')

    def start(self, screen, edit_level, index):

        e_offset = 75 / 2

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

        self.delete_button = Button([self.screen_x - 90, self.screen_y - 135], BUTTON_SIZE, BUTTON_SIZE, 'Delete', 25, screen)
        self.save_button = Button([self.screen_x - 90, self.screen_y - 405], BUTTON_SIZE, BUTTON_SIZE, 'Save', 30, screen)
        self.save_button.disabled = True
        self.cancel_buttton = Button([self.screen_x - 90, self.screen_y - 270], BUTTON_SIZE, BUTTON_SIZE, 'Cancel', 27, screen)

        if edit_level is not None and index is not None:
            self.editing = True
            self.player_start = edit_level.player_start
            self.sprites = edit_level.level_group
            self.enemies = edit_level.enemies
            self.objects = edit_level.objects
            self.ending = [edit_level.ending.rect.x, edit_level.ending.rect.y]
        else: self.delete_button.disabled = True

        while self.level_creator_is_active:

            mouse_pos = pygame.mouse.get_pos()
            button_clicks = self.__calculate_button_clicks(mouse_pos)
            all_sprites = self.sprites.copy()
            all_sprites.add(self.enemies)
            all_sprites.add(self.objects)

            if self.save_button.disabled and self.player_start is not None and self.ending is not None and len(self.sprites) > 0: self.save_button.disabled = False

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
                            self.player_start = [mouse_pos[0] + self.offset[0] - 75, mouse_pos[1] + self.offset[1] - 75]
                        elif self.type == Creation_Type.ENEMY:
                            self.enemies.add(Enemy([mouse_pos[0] + self.offset[0] - e_offset, mouse_pos[1] + self.offset[1] - e_offset], screen))
                        elif self.type == Creation_Type.ENDING:
                            self.ending = [mouse_pos[0] + self.offset[0] - 100, mouse_pos[1] + self.offset[1] - 100]
                        elif self.type == Creation_Type.OBJECT:
                            self.objects.add(Movable_Object([mouse_pos[0] + self.offset[0] - 50, mouse_pos[1] + self.offset[1] - 50]))
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
                        break;

            # Reset camera
            if keys[pygame.K_SPACE]:
                self.offset = [75 + self.player_start[0] - self.screen_x / 2, 75 + self.player_start[1] - self.screen_y / 2] if self.player_start is not None else [0, 0]

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
            if button_clicks[7]:
                self.delete = True

            # Save the file
            if button_clicks[5] or self.delete:
                level_path = Path('levels/levels.lvl')
                if not self.editing:
                    with level_path.open(mode='a+') as file:
                        file.write(u'*LEVEL*\n')
                        file.write(u'PLS$[%d,%d]\n' % (self.player_start[0], self.player_start[1]))
                        for platform in self.sprites: file.write(u'PLA$[%d,%d]$%d$%d$#000000\n' % (platform.position[0], platform.position[1], platform.width, platform.height))
                        for enemy in self.enemies: file.write(u'ENE$[%d,%d]\n' % (enemy.pos[0], enemy.pos[1]))
                        for object in self.objects: file.write(u'OBJ$[%d,%d]\n' % (object.pos[0], object.pos[1]))
                        file.write(u'END$[%d,%d]\n' % (self.ending[0], self.ending[1]))
                else:
                    data = None
                    with level_path.open(mode='r+') as f: data = str(f.read()).split('*LEVEL*\n')
                    del data[0]
                    for d in range(len(data)): data[d] = '*LEVEL*\n' + data[d]
                    if not self.delete:
                        data[index] = '*LEVEL*\n'
                        data[index] += 'PLS$[%d,%d]\n' % (self.player_start[0], self.player_start[1])
                        for platform in self.sprites: data[index] += 'PLA$[%d,%d]$%d$%d$#000000\n' % (platform.position[0], platform.position[1], platform.width, platform.height)
                        for enemy in self.enemies: data[index] += 'ENE$[%d,%d]\n' % (enemy.pos[0], enemy.pos[1])
                        for object in self.objects: data[index] += 'OBJ$[%d,%d]\n' % (object.pos[0], object.pos[1])
                        data[index] += 'END$[%d,%d]\n' % (self.ending[0], self.ending[1])
                    else:
                        del data[index]
                    with level_path.open(mode='w+') as f: f.write(unicode(''.join(data)))
                self.level_creator_is_active = False
                return

            if button_clicks[6]:
                self.level_creator_is_active = False
                return

            # If the delete button is enabled
            if (keys[pygame.K_RSHIFT] | keys[pygame.K_LSHIFT]) and edit_level is not None and index is not None:
                self.delete_button.disabled = False
            else: self.delete_button.disabled = True

            # Draw sky
            screen.fill(pygame.Color('lightblue'))
            screen.blit(self.SUN, (50, 50))

            # Draw and offset platforms
            for sprite in all_sprites:
                sprite.rect.x -= self.offset[0]
                sprite.rect.y -= self.offset[1]

            all_sprites.draw(screen)

            if len(all_sprites) == 0: self.save_button.disabled = True

            for sprite in all_sprites:
                sprite.rect.x += self.offset[0]
                sprite.rect.y += self.offset[1]

            if self.player_start != None:
                s = pygame.Surface((150, 150))
                s.blit(self.PLAYER_IMAGE, s.get_rect())
                screen.blit(s, [self.player_start[0] - self.offset[0], self.player_start[1] - self.offset[1]])

            if self.ending != None:
                s = pygame.Surface((200, 200))
                s.fill(pygame.Color('green'))
                screen.blit(s, [self.ending[0] - self.offset[0], self.ending[1] - self.offset[1]])

            # Draw preview
            if self.type == Creation_Type.PLAYER:
                s = pygame.Surface((150, 150))
                s.set_alpha(128)
                s.blit(self.PLAYER_IMAGE, s.get_rect())
                screen.blit(s, (mouse_pos[0] - 75, mouse_pos[1] - 75))
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
                s.blit(self.ENEMY_IMAGE, s.get_rect())
                screen.blit(s, (mouse_pos[0] - e_offset, mouse_pos[1] - e_offset))
            elif self.type == Creation_Type.ENDING:
                s = pygame.Surface((200, 200))
                s.set_alpha(128)
                s.fill(pygame.Color('green'))
                screen.blit(s, (mouse_pos[0] - 100, mouse_pos[1] - 100))
            elif self.type == Creation_Type.OBJECT:
                s = pygame.Surface((100, 100))
                s.set_alpha(128)
                s.fill(pygame.Color('red'))
                screen.blit(s, (mouse_pos[0] - 50, mouse_pos[1] - 50))

            self.set_player_start_button.draw()
            self.set_platform_button.draw()
            self.set_enemy_button.draw()
            self.set_ending_button.draw()
            self.set_object_button.draw()
            self.delete_button.draw()
            self.save_button.draw()
            self.cancel_buttton.draw()

            if self.SHOW_FPS: screen.blit(self.fps_font.render(str(int(clock.get_fps())), True, pygame.Color('white'), pygame.Color('black')), (0, 0))

            pygame.display.flip()
            clock.tick(self.FPS)

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
        return [self.set_player_start_button.check_click(mouse_pos[0], mouse_pos[1]), self.set_platform_button.check_click(mouse_pos[0], mouse_pos[1]), self.set_enemy_button.check_click(mouse_pos[0], mouse_pos[1]), self.set_ending_button.check_click(mouse_pos[0], mouse_pos[1]), self.set_object_button.check_click(mouse_pos[0], mouse_pos[1]), self.save_button.check_click(mouse_pos[0], mouse_pos[1]),  self.cancel_buttton.check_click(mouse_pos[0], mouse_pos[1]), self.delete_button.check_click(mouse_pos[0], mouse_pos[1])]

    def stop(self):
        if self.VERBOSE: print('Halt signal recieved, creator closing')
        self.level_creator_is_active = False
        return
