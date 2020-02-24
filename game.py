import pygame
import sys
from player import Player
from game_platform import Platform
from cloud import Cloud
import __main__ as m
from itertools import islice
from enemy import Enemy

'''
This Class is the game itself. All of the different game classes come together here.
'''
class Game(object):

    # Class initializer
    def __init__(self, levels, update, VERBOSE, DEBUG, NOAI, NOAUDIO, SHOW_FPS):
        super(Game, self).__init__()
        self.levels = levels
        self.update = update
        self.VERBOSE = VERBOSE
        self.DEBUG = DEBUG
        self.no_ai = NOAI
        self.NOAUDIO = NOAUDIO
        self.SHOW_FPS = SHOW_FPS

        # Total camera movement in both the x and y directions
        self.total_offset_x = 0
        self.total_offset_y = 0
        self.initial_move_offset_x = 0
        self.initial_move_offset_y = 0

        # Free camera variables
        self.free_camera_movement = False
        self.total_free_camera_offset_x = 0
        self.total_free_camera_offset_y = 0

        # Constants
        self.GRAVITY = .19
        self.FPS = 60
        self.PARALAX_RATIO = 3

        # Sounds
        if not self.NOAUDIO:
            self.JUMP_ENEMY = pygame.mixer.Sound('audio/jump_enemy.wav')
            self.JUMP = pygame.mixer.Sound('audio/jump.wav')

        # Load images
        self.ENEMY_IMAGE = pygame.image.load('images/enemy.png')
        self.ENEMY_REVERSED = pygame.image.load('images/enemy_reversed.png')
        self.PLAYER_SLAMMING_REVERSED = pygame.image.load('images/player_slamming_reversed.png')
        self.PLAYER_SLAMMING = pygame.image.load('images/player_slamming.png')
        self.PLAYER_REVERSED = pygame.image.load('images/player_reversed.png')
        self.PLAYER_IMAGE = pygame.image.load('images/player.png')
        self.SUN = pygame.image.load('images/sun.png')

        # Load fonts
        self.fps_font = pygame.font.Font('fonts/FreeSansBold.ttf', 20)

        if self.VERBOSE: print 'Game initialized'

    # Start the game
    def start(self, screen):

        # Screen setup
        clock = pygame.time.Clock()
        screen_x, screen_y = pygame.display.get_surface().get_size()
        self.SCREEN_SIZE = [screen_x, screen_y]
        pygame.mouse.set_visible(False)

        if self.VERBOSE: print 'Display initialized'

        # Loops through all levels
        for level in islice(self.levels, m.current_level, None):

            # Initialize level
            horizontal_constraints = [level.least_x, level.greatest_x]
            vertical_constraints = [level.least_y, level.greatest_y]
            player = Player(level.player_start, screen)
            player_group = pygame.sprite.Group()
            player_group.add(player)
            self.game_is_running = True
            if (self.no_ai):
                level.disable_ai()
                print 'Game starting with enemy AI disabled'

            # Create rectangles for lives (I just felt like using long variable names)
            life_rect_size = 20
            life_rect_distance_from_edges_of_screen = 10
            life_rect_x_gap = 10
            current_top_left_of_life_rect = [screen_x - life_rect_distance_from_edges_of_screen - life_rect_size, life_rect_distance_from_edges_of_screen]
            life_rects = []
            for _ in range(player.lives):
                life_rect = pygame.Rect(current_top_left_of_life_rect, (life_rect_size, life_rect_size))
                life_rects.append(life_rect)
                current_top_left_of_life_rect[0] -= life_rect_x_gap + life_rect_size

            # Make clouds
            level.set_clouds(Cloud(screen, self.SCREEN_SIZE[0], self.SCREEN_SIZE[1], horizontal_constraints, vertical_constraints, self.VERBOSE).clouds)

            # Calculate initial offset
            self.initial_move_offset_x = -player_start[0]
            self.initial_move_offset_y = -player_start[1]

            if self.VERBOSE: print 'Level initialized'

            # Main game loop
            if self.VERBOSE: print 'Starting main game loop'
            while self.game_is_running:

                # Handle events
                for event in pygame.event.get():

                    # If user quits
                    if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        if self.VERBOSE: print 'Gameplay stopped, returning to main menu'
                        return

                '''
                Game logic
                '''

                # Loop through enemies
                for enemy in level.enemies:

                    # Check if enemy is below level
                    if enemy.rect.top > vertical_constraints[1]: enemy.kill()

                    # Enemy group without current enemy
                    exclusive_enemy_group = level.enemies.copy()
                    exclusive_enemy_group.remove(enemy)

                    # If enemy collides with player
                    is_collide = False

                    # Horizontal logic
                    enemy.prev_x = enemy.rect.x
                    if not self.no_ai and enemy.is_enabled:
                        if enemy.rect.centerx < player.rect.centerx:
                            enemy.rect.x += enemy.speed
                            if enemy.rect.centerx > player.rect.centerx:
                                enemy.rect.centerx = player.rect.centerx
                        elif enemy.rect.centerx > player.rect.centerx:
                            enemy.rect.x -= enemy.speed
                            if enemy.rect.centerx < player.rect.centerx:
                                enemy.rect.centerx = player.rect.centerx

                    # Bound to horizontal constraints
                    if enemy.rect.left < horizontal_constraints[0]:
                        enemy.rect.left = horizontal_constraints[0]
                    if enemy.rect.right > horizontal_constraints[1]:
                        enemy.rect.right = horizontal_constraints[1]
                    if enemy.prev_x < enemy.rect.x:
                        enemy.image = self.ENEMY_IMAGE
                    elif enemy.prev_x > enemy.rect.x:
                        enemy.image = self.ENEMY_REVERSED

                    # Horizontal collisions
                    if enemy.is_enabled:
                        collisions = pygame.sprite.spritecollide(enemy, level.level_group, False) + pygame.sprite.spritecollide(enemy, exclusive_enemy_group, False) + pygame.sprite.spritecollide(enemy, player_group, False) + pygame.sprite.spritecollide(enemy, level.objects, False)
                        for collision in collisions:
                            if isinstance(collision, Player): is_collide = True
                            if enemy.prev_x > enemy.rect.x:
                                enemy.rect.left = collision.rect.right
                            elif enemy.prev_x < enemy.rect.x:
                                enemy.rect.right = collision.rect.left

                    # Whether or not the enemy should jump
                    jump = False
                    if enemy.is_enabled and (len(collisions) > 1 or (len(collisions) == 1 and not isinstance(collisions[0], Player))): jump = True

                    # Vertical logic
                    enemy.prev_y = enemy.rect.y
                    if jump: enemy.jump()
                    enemy.vertical_acceleration += self.GRAVITY
                    enemy.rect.y += enemy.vertical_acceleration

                    # Vertical collisions
                    if enemy.is_enabled:
                        collisions = pygame.sprite.spritecollide(enemy, level.level_group, False) + pygame.sprite.spritecollide(enemy, level.objects, False)  + pygame.sprite.spritecollide(enemy, exclusive_enemy_group, False) + pygame.sprite.spritecollide(enemy, player_group, False)
                        for collision in collisions:
                            if isinstance(collision, Player): is_collide = True
                            if enemy.prev_y > enemy.rect.y:
                                enemy.rect.top = collision.rect.bottom
                            elif enemy.prev_y < enemy.rect.y:
                                enemy.rect.bottom = collision.rect.top
                                enemy.is_in_air = False
                            enemy.vertical_acceleration = 0
                        if enemy.vertical_acceleration != 0: enemy.is_in_air = True

                    # Get rid of player health
                    if is_collide: player.health -= 1

                # Handle objects
                for object in level.objects:

                    # Kill if it goes too low
                    if object.rect.top > vertical_constraints[1]:
                        object.kill()
                        continue

                    # Move horizontally
                    object.prev_x = object.rect.x
                    object.rect.x += object.delta
                    for collision in pygame.sprite.spritecollide(object, level.level_group, False):
                        if object.prev_x < object.rect.x:
                            object.rect.right = collision.rect.left
                        elif object.prev_x > object.rect.x:
                            object.rect.left = collision.rect.right

                    # Bound to walls
                    if object.rect.left < horizontal_constraints[0]:
                        object.rect.left = horizontal_constraints[0]
                    if object.rect.right > horizontal_constraints[1]:
                        object.rect.right = horizontal_constraints[1]

                    object.delta = 0

                    # Gravity
                    object.prev_y = object.rect.y
                    object.vertical_acceleration += self.GRAVITY
                    object.rect.y += object.vertical_acceleration
                    g = level.level_group.copy()
                    g.add(level.objects)
                    g.remove(object)
                    for collision in pygame.sprite.spritecollide(object, g, False):
                        if object.prev_y < collision.rect.top:
                            object.rect.bottom = collision.rect.top
                        else:
                            object.rect.top = collision.rect.bottom
                        object.vertical_acceleration = 0
                    for collision in pygame.sprite.spritecollide(object, player_group, False):
                        if object.prev_y < collision.rect.top:
                            object.rect.bottom = collision.rect.top
                            object.vertical_acceleration = 0

                '''
                Player logic
                '''

                # Keys pressed
                keys = pygame.key.get_pressed()
                key_w = True if keys[pygame.K_w] or keys[pygame.K_UP] else False
                key_a = True if keys[pygame.K_a] or keys[pygame.K_LEFT] else False
                key_s = True if keys[pygame.K_s] or keys[pygame.K_DOWN] else False
                key_d = True if keys[pygame.K_d] or keys[pygame.K_RIGHT] else False
                key_SPACE = keys[pygame.K_SPACE]

                # Horizontal logic
                player.prev_x = player.rect.x
                if key_d and not self.free_camera_movement:
                    player.rect.x += player.speed
                if key_a and not self.free_camera_movement:
                    player.rect.x -= player.speed

                # Loop through all horizontal platform collisions
                self.check_collide(player, level.level_group, 'x')

                # Move enemies horizontally
                collisions = pygame.sprite.spritecollide(player, level.enemies, False)
                for enemy in collisions:
                    if not enemy.is_enabled: continue
                    enemy_prev_x = enemy.rect.x
                    if player.prev_x > player.rect.x:
                        enemy.rect.right = player.rect.left
                    elif player.prev_x < player.rect.x:
                        enemy.rect.left = player.rect.right
                    if pygame.sprite.spritecollideany(enemy, level.objects, False) or pygame.sprite.spritecollideany(enemy, level.level_group, False):
                        enemy.rect.x = enemy_prev_x
                        player.rect.x = player.prev_x

                # Move blocks
                if not self.free_camera_movement:
                    for collision in pygame.sprite.spritecollide(player, level.objects, False):
                        if player.prev_x < collision.rect.centerx:
                            player.rect.right = collision.rect.left
                            collision.delta = player.speed
                        elif player.prev_x > collision.rect.centerx:
                            player.rect.left = collision.rect.right
                            collision.delta = -player.speed

                # Bound to walls
                if player.rect.left < horizontal_constraints[0]:
                    player.rect.left = horizontal_constraints[0]
                if player.rect.right > horizontal_constraints[1]:
                    player.rect.right = horizontal_constraints[1]

                if not self.free_camera_movement and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    player.vertical_acceleration += 4
                    player.is_slamming = True
                else: player.is_slamming = False

                # Vertical logic
                if (key_w or key_SPACE) and not player.is_in_air and not player.is_slamming and not self.free_camera_movement:
                    if not self.NOAUDIO: self.JUMP.play()
                    player.vertical_acceleration -= 9
                    player.is_in_air = True

                # Change y values
                player.prev_y = player.rect.y
                player.vertical_acceleration += self.GRAVITY
                player.rect.y += player.vertical_acceleration

                # Loop through all vertical static collision
                self.check_collide(player, level.level_group, 'y')
                self.check_collide(player, level.objects, 'y')
                if player.vertical_acceleration != 0: player.is_in_air = True

                # Loop through all vertical enemy collisions
                collisions = pygame.sprite.spritecollide(player, level.enemies, False)
                for enemy in collisions:
                    if not enemy.is_enabled: continue
                    if player.prev_y < player.rect.y:
                        if player.is_slamming:
                            if enemy.is_in_air:
                                enemy.rect.top = player.rect.bottom
                                if pygame.sprite.spritecollideany(enemy, level.level_group, False) or pygame.sprite.spritecollide(enemy, level.objects, False): enemy.kill_by_player()
                            else: enemy.kill_by_player()
                        else:
                            player.rect.bottom = enemy.rect.top
                            player.is_in_air = False
                    elif player.prev_y > player.rect.y:
                        enemy.rect.bottom = player.rect.top

                # Change player image depending on direcion moved
                if player.prev_x < player.rect.x:
                    player.direction = 'r'
                elif player.prev_x > player.rect.x:
                    player.direction = 'l'

                if player.is_slamming:
                    if player.direction == 'l':
                        player.image = self.PLAYER_SLAMMING_REVERSED
                    elif player.direction == 'r':
                        player.image = self.PLAYER_SLAMMING
                else:
                    if player.direction == 'l':
                        player.image = self.PLAYER_REVERSED
                    elif player.direction == 'r':
                        player.image = self.PLAYER_IMAGE

                # Debug keys
                if self.DEBUG:

                    # Start or stop rendering
                    if keys[pygame.K_o]:
                        level.start_render()
                    if keys[pygame.K_p]:
                        level.stop_render()

                    # Start or stop enemy movement
                    if keys[pygame.K_MINUS]:
                        level.disable_ai()
                        self.no_ai = True
                    if keys[pygame.K_EQUALS]:
                        level.enable_ai()
                        self.no_ai = False

                    # Start or stop free camera movement
                    if keys[pygame.K_F1] and not self.free_camera_movement:
                        self.total_free_camera_offset_x = 0
                        self.total_free_camera_offset_y = 0
                        self.free_camera_movement = True
                        print 'Free camera movement enabled'
                    if keys[pygame.K_F2] and self.free_camera_movement:

                        # Reset camera
                        player.rect.x -= self.total_free_camera_offset_x
                        horizontal_constraints[0] -= self.total_free_camera_offset_x
                        horizontal_constraints[1] -= self.total_free_camera_offset_x
                        level.ending.rect.x -= self.total_free_camera_offset_x
                        player.rect.y -= self.total_free_camera_offset_y
                        vertical_constraints[0] -= self.total_free_camera_offset_y
                        vertical_constraints[1] -= self.total_free_camera_offset_y
                        level.ending.rect.y -= self.total_free_camera_offset_y
                        for cloud in level.clouds:
                            cloud.rect.x -= self.total_free_camera_offset_x / self.PARALAX_RATIO
                            cloud.rect.y -= self.total_free_camera_offset_y / self.PARALAX_RATIO
                        for platform_sprite in level.level_group:
                            platform_sprite.rect.x -= self.total_free_camera_offset_x
                            platform_sprite.rect.y -= self.total_free_camera_offset_y
                        for enemy in level.enemies:
                            enemy.rect.x -= self.total_free_camera_offset_x
                            enemy.rect.y -= self.total_free_camera_offset_y
                        for object in level.objects:
                            object.rect.x -= self.total_free_camera_offset_x
                            object.rect.y -= self.total_free_camera_offset_y
                        self.free_camera_movement = False
                        print 'Free camera movement disabled'

                '''
                Camera logic
                '''

                offset_x = 0
                offset_y = 0

                if self.free_camera_movement:
                    if key_d:
                        offset_x -= player.speed
                    if key_a:
                        offset_x += player.speed
                    if key_w:
                        offset_y += player.speed
                    if key_s:
                        offset_y -= player.speed
                    if keys[pygame.L_SHIFT] or keys[pygame.R_SHIFT]:
                        offset_x *= 2
                        offset_y *= 2

                    self.total_free_camera_offset_x += offset_x
                    self.total_free_camera_offset_y += offset_y

                # Move camera horizontally
                if not self.free_camera_movement and player.rect.centerx > horizontal_constraints[0] + (self.SCREEN_SIZE[0] / 2) and player.rect.centerx < horizontal_constraints[1] - (self.SCREEN_SIZE[0] / 2):
                    if player.rect.x > player.prev_x:
                        s = player.rect.x - player.prev_x
                        offset_x -= s
                        player.rect.x -= s
                        horizontal_constraints[0] -= s
                        horizontal_constraints[1] -= s
                        level.ending.rect.x -= s
                    elif player.rect.x < player.prev_x:
                        s = player.prev_x - player.rect.x
                        offset_x += s
                        player.rect.x += s
                        horizontal_constraints[0] += s
                        horizontal_constraints[1] += s
                        level.ending.rect.x += s
                elif self.free_camera_movement:
                    player.rect.x += offset_x
                    horizontal_constraints[0] += offset_x
                    horizontal_constraints[1] += offset_x
                    level.ending.rect.x += offset_x

                # Move camera vertically
                if not self.free_camera_movement and player.rect.centery > vertical_constraints[0] + (self.SCREEN_SIZE[1] / 2) and player.rect.centery < vertical_constraints[1] - (self.SCREEN_SIZE[1] / 2) and player.prev_y != player.rect.y:
                    offset_y = self.SCREEN_SIZE[1] / 2 - player.rect.centery
                    player.rect.y += offset_y
                    vertical_constraints[0] += offset_y
                    vertical_constraints[1] += offset_y
                    level.ending.rect.y += offset_y
                elif self.free_camera_movement:
                    player.rect.y += offset_y
                    vertical_constraints[0] += offset_y
                    vertical_constraints[1] += offset_y
                    level.ending.rect.y += offset_y

                if offset_x != 0 or offset_y != 0:

                    # Loop through all clouds
                    for cloud in level.clouds:
                        cloud.rect.x += offset_x / self.PARALAX_RATIO
                        cloud.rect.y += offset_y / self.PARALAX_RATIO

                    # Loop through all of the level's platforms
                    for platform_sprite in level.level_group:
                        platform_sprite.rect.x += offset_x
                        platform_sprite.rect.y += offset_y

                    # Loop through all of the level's enemies
                    for enemy in level.enemies:
                        enemy.rect.x += offset_x
                        enemy.rect.y += offset_y

                    # Loop through all of the level's objects
                    for object in level.objects:
                        object.rect.x += offset_x
                        object.rect.y += offset_y

                    # Add to total
                    self.total_offset_x += offset_x
                    self.total_offset_y += offset_y

                # Check if level passed
                level.update()
                if player.rect.colliderect(level.ending.rect) and not level.ending.locked:
                    self.game_is_running = False
                    self.update(m)

                # Check if player died
                if player.rect.top > vertical_constraints[1] or player.health <= 0:
                    if player.lives <= 0:
                        player.kill()
                        if self.VERBOSE: print 'Player died. Gameplay stopped, returning to main menu.'
                        return
                    else:
                        player.lives -= 1
                        player.health = player.max_health
                        life_rects.pop()
                        if self.VERBOSE: print 'Player died. %d lives remaining.' % player.lives
                        horizontal_constraints[0] -= self.total_offset_x
                        horizontal_constraints[1] -= self.total_offset_x
                        level.ending.rect.x -= self.total_offset_x
                        vertical_constraints[0] -= self.total_offset_y
                        vertical_constraints[1] -= self.total_offset_y
                        level.ending.rect.y -= self.total_offset_y
                        for cloud in level.clouds:
                            cloud.rect.x -= self.total_offset_x / self.PARALAX_RATIO
                            cloud.rect.y -= self.total_offset_y / self.PARALAX_RATIO
                        for platform_sprite in level.level_group:
                            platform_sprite.rect.x -= self.total_offset_x
                            platform_sprite.rect.y -= self.total_offset_y
                        for enemy in level.enemies:
                            enemy.rect.x -= self.total_offset_x
                            enemy.rect.y -= self.total_offset_y
                        for object in level.objects:
                            object.rect.x -= self.total_offset_x
                            object.rect.y -= self.total_offset_y
                        player.rect.x = level.player_start[0]
                        player.rect.y = level.player_start[1]
                        player.vertical_acceleration = 0
                        self.total_offset_x = 0
                        self.total_offset_y = 0

                '''
                All game drawing
                '''

                # Draw sky
                screen.fill(pygame.Color('lightblue'))
                screen.blit(self.SUN, (50, 50))

                # Draw foreground items
                level.draw()
                player_group.draw(screen)

                # Draw health bar
                health_bar_size = 20
                health_bar_multiplier = 5
                health_bar_border = 5
                health_bar_x = (screen_x / 2) - (health_bar_multiplier * 100)
                health_bar_y = screen_y - health_bar_size
                health_rect_background = pygame.Rect(health_bar_x - health_bar_border, health_bar_y - (health_bar_border * 2) - 2, (health_bar_multiplier * player.max_health) + (health_bar_border * 2), health_bar_size + (health_bar_border * 2))
                health_rect = pygame.Rect(health_bar_x, health_bar_y - health_bar_border - 2, health_bar_multiplier * player.health, health_bar_size)
                pygame.draw.rect(screen, (0, 0, 0), health_rect_background, 0)
                pygame.draw.rect(screen, pygame.Color('red'), health_rect, 0)

                # Draw life rects
                for life_rect in life_rects:
                    pygame.draw.rect(screen, (32, 177, 75), life_rect)

                if self.SHOW_FPS: screen.blit(self.fps_font.render(str(int(clock.get_fps())), True, pygame.Color('white'), pygame.Color('black')), (0, 0))

                # Update display
                pygame.display.flip()

                # Set frame rate
                clock.tick(self.FPS)

        if self.VERBOSE: print 'Gameplay stopped, returning to main menu'
        return

    def check_collide(self, sprite, group, dir):
        collision = pygame.sprite.spritecollideany(sprite, group, False)
        if collision:
            if dir == 'x':
                if sprite.prev_x < collision.rect.centerx:
                    sprite.rect.right = collision.rect.left
                elif sprite.prev_x > collision.rect.centerx:
                    sprite.rect.left = collision.rect.right
                self.check_collide(sprite, group, dir)
            elif dir == 'y':
                if sprite.prev_y < collision.rect.centery:
                    sprite.rect.bottom = collision.rect.top
                    sprite.is_in_air = False
                elif sprite.prev_y > collision.rect.centery:
                    sprite.rect.top = collision.rect.bottom
                sprite.vertical_acceleration = 0
        else: return
