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
    def __init__(self, levels, update, verbose, debug):
        super(Game, self).__init__()
        self.levels = levels
        self.update = update
        self.VERBOSE = verbose
        self.DEBUG = debug

        # Constants
        self.GRAVITY = .19
        self.FPS = 60
        self.PARALAX_RATIO = 3

        # Sounds
        self.JUMP_ENEMY = pygame.mixer.Sound('jump_enemy.wav')
        self.JUMP = pygame.mixer.Sound('jump.wav')

        if self.VERBOSE: print 'Game initialized'

    # Start the game
    def start(self, screen):

        # Screen setup
        clock = pygame.time.Clock()
        screen_x, screen_y = pygame.display.get_surface().get_size()
        self.SCREEN_SIZE = [screen_x, screen_y]

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
            if self.VERBOSE: print 'Level initialized'

            # Make clouds
            level.set_clouds(Cloud(screen, self.SCREEN_SIZE[0], self.SCREEN_SIZE[1], horizontal_constraints, vertical_constraints, self.VERBOSE).clouds)

            # Main game loop
            if self.VERBOSE: print 'Initializing main game loop'
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

                    is_player_x_collide = len(pygame.sprite.spritecollide(enemy, player_group, False)) > 0
                    is_x_collide = False

                    if enemy.is_enabled:

                        exclusive_enemy_group = level.enemies.copy()
                        exclusive_enemy_group.remove(enemy)

                        # Move horizontally
                        enemy.prev_x = enemy.rect.x
                        if enemy.has_ai:
                            if enemy.rect.centerx < player.rect.centerx:
                                enemy.rect.x += abs(enemy.speed)
                            elif enemy.rect.centerx > player.rect.centerx:
                                enemy.rect.x -= abs(enemy.speed)

                        # Loop through all horizontal collisions
                        collisions = pygame.sprite.spritecollide(enemy, level.level_group, False) + pygame.sprite.spritecollide(enemy, player_group, False) + pygame.sprite.spritecollide(enemy, exclusive_enemy_group, False) + pygame.sprite.spritecollide(enemy, level.objects, False)
                        for collision in collisions:
                            if isinstance(collision, Enemy) and not collision.is_enabled: continue
                            if not is_x_collide and not isinstance(collision, Enemy): is_x_collide = True
                            if enemy.prev_x < enemy.rect.x:
                                enemy.rect.right = collision.rect.left
                            elif enemy.prev_x > enemy.rect.x:
                                enemy.rect.left = collision.rect.right

                        # Bound to constraints
                        if enemy.rect.left < horizontal_constraints[0]:
                            enemy.rect.left = horizontal_constraints[0]
                        if enemy.rect.right > horizontal_constraints[1]:
                            enemy.rect.right = horizontal_constraints[1]
                        if enemy.prev_x < enemy.rect.x:
                            enemy.image = pygame.image.load('enemy.png')
                        elif enemy.prev_x > enemy.rect.x:
                            enemy.image = pygame.image.load('enemy_reversed.png')

                    # Move vertically
                    enemy.prev_y = enemy.rect.y
                    if is_x_collide and enemy.is_enabled and enemy.has_ai: enemy.jump()
                    enemy.vertical_acceleration += self.GRAVITY
                    enemy.rect.y += enemy.vertical_acceleration
                    if enemy.is_enabled:

                        collisions = pygame.sprite.spritecollide(enemy, level.level_group, False) + pygame.sprite.spritecollide(enemy, exclusive_enemy_group, False) + pygame.sprite.spritecollide(enemy, level.objects, False)

                        # Loop through all vertical collisions
                        is_player_y_collide = len(pygame.sprite.spritecollide(enemy, player_group, False)) > 0
                        for collision in collisions:
                            if isinstance(collision, Enemy) and not collision.is_enabled: continue
                            if enemy.prev_y < enemy.rect.y:
                                enemy.rect.bottom = collision.rect.top
                                enemy.is_in_air = False
                            elif enemy.prev_y > enemy.rect.y: enemy.rect.top = collision.rect.bottom
                            enemy.vertical_acceleration = 0
                        if enemy.vertical_acceleration != 0: enemy.is_in_air = True

                    # Check if enemy died
                    if enemy.rect.centery > vertical_constraints[1]:
                        enemy.kill()
                        continue
                    if is_player_x_collide or is_player_y_collide and enemy.is_enabled: player.health -= 1

                # Handle objects
                for object in level.objects:

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

                # Horizontal logic
                player.prev_x = player.rect.x
                keys = pygame.key.get_pressed()
                if keys[pygame.K_d]:
                    player.rect.x += player.speed
                if keys[pygame.K_a]:
                    player.rect.x -= player.speed
                collisions = pygame.sprite.spritecollide(player, level.level_group, False)

                # Loop through all horizontal platform collisions
                for collision in collisions:
                    if keys[pygame.K_d] and not keys[pygame.K_a]:
                        player.rect.right = collision.rect.left
                    elif keys[pygame.K_a] and not keys[pygame.K_d]:
                        player.rect.left = collision.rect.right

                # Move blocks
                for collision in pygame.sprite.spritecollide(player, level.objects, False):
                    if keys[pygame.K_d] and not keys[pygame.K_a]:
                        player.rect.right = collision.rect.left
                        collision.delta = player.speed
                    elif keys[pygame.K_a] and not keys[pygame.K_d]:
                        player.rect.left = collision.rect.right
                        collision.delta = -player.speed

                # Move colliding enemies horizontally
                for enemy in pygame.sprite.spritecollide(player, level.enemies, False):
                    enemy_prev_pos = enemy.rect.x
                    if keys[pygame.K_d] and not keys[pygame.K_a]:
                        enemy.rect.left = player.rect.right
                    elif keys[pygame.K_a] and not keys[pygame.K_d]:
                        enemy.rect.right = player.rect.left
                    if pygame.sprite.spritecollideany(enemy, level.level_group) != None or pygame.sprite.spritecollideany(enemy, level.objects) != None:
                        enemy.rect.x = enemy_prev_pos
                    if enemy.rect.left < horizontal_constraints[0] or enemy.rect.right > horizontal_constraints[1]:
                        enemy.kill_by_player()

                # Bound to walls
                if player.rect.left < horizontal_constraints[0]:
                    player.rect.left = horizontal_constraints[0]
                if player.rect.right > horizontal_constraints[1]:
                    player.rect.right = horizontal_constraints[1]

                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    player.vertical_acceleration += 4
                    player.is_slamming = True
                else: player.is_slamming = False

                # Vertical logic
                if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and not player.is_in_air and not player.is_slamming:
                    self.JUMP.play()
                    player.vertical_acceleration -= 9
                    player.is_in_air = True

                # Change y values
                player.prev_y = player.rect.y
                player.vertical_acceleration += self.GRAVITY
                player.rect.y += player.vertical_acceleration

                collisions = pygame.sprite.spritecollide(player, level.level_group, False) + pygame.sprite.spritecollide(player, level.objects, False)

                # Loop through all vertical collisions
                for collision in collisions:
                    if player.prev_y < collision.rect.top:
                        player.rect.bottom = collision.rect.top
                        player.is_in_air = False
                    else:
                        player.rect.top = collision.rect.bottom
                    player.vertical_acceleration = 0
                if player.vertical_acceleration != 0: player.is_in_air = True

                # Handle enemy and player collisions
                for enemy in pygame.sprite.spritecollide(player, level.enemies, False):
                    if enemy.rect.top > player.rect.centery:
                        if player.is_slamming:
                            if not enemy.is_in_air:
                                enemy.kill_by_player()
                                enemy.image = pygame.image.load('enemy_dead.png')
                            else:
                                enemy.rect.top = player.rect.bottom
                        else:
                            if not enemy.is_in_air:
                                enemy.rect.top = player.rect.bottom
                            else:
                                player.rect.bottom = enemy.rect.top

                # Change player image depending on direcion moved
                if player.prev_x < player.rect.x:
                    player.image = pygame.image.load('player.png')
                elif player.prev_x > player.rect.x:
                    player.image = pygame.image.load('player_reversed.png')

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
                    if keys[pygame.K_EQUALS]:
                        level.enable_ai()

                # Player kill
                if player.health <= 0:
                    player.kill
                    if self.VERBOSE: print 'Gameplay stopped, returning to main menu'
                    return

                '''
                Camera logic
                '''

                offset_x = 0
                offset_y = 0

                # Move camera horizontally
                if player.rect.centerx > horizontal_constraints[0] + (self.SCREEN_SIZE[0] / 2) and player.rect.centerx < horizontal_constraints[1] - (self.SCREEN_SIZE[0] / 2):
                    if player.rect.x > player.prev_x:
                        offset_x -= player.speed
                        player.rect.x -= player.speed
                        horizontal_constraints[0] -= player.speed
                        horizontal_constraints[1] -= player.speed
                        level.ending.rect.x -= player.speed
                    elif player.rect.x < player.prev_x:
                        offset_x += player.speed
                        player.rect.x += player.speed
                        horizontal_constraints[0] += player.speed
                        horizontal_constraints[1] += player.speed
                        level.ending.rect.x += player.speed

                # Move camera vertically
                if player.rect.centery > vertical_constraints[0] + (self.SCREEN_SIZE[1] / 2) and player.rect.centery < vertical_constraints[1] - (self.SCREEN_SIZE[1] / 2) and player.prev_y != player.rect.y:
                    offset_y = self.SCREEN_SIZE[1] / 2 - player.rect.centery
                    player.rect.y += offset_y
                    vertical_constraints[0] += offset_y
                    vertical_constraints[1] += offset_y
                    level.ending.rect.y += offset_y

                if offset_x != 0 or offset_y != 0:

                    # Loop through all clouds
                    for cloud in level.clouds:
                        cloud.rect.x += offset_x / self.PARALAX_RATIO
                        cloud.rect.y += offset_y / self.PARALAX_RATIO

                    # Loop through all of the level's sprites
                    for platform_sprite in level.level_group:
                        platform_sprite.rect.x += offset_x
                        platform_sprite.rect.y += offset_y
                    for enemy in level.enemies:
                        enemy.rect.x += offset_x
                        enemy.rect.y += offset_y
                    for object in level.objects:
                        object.rect.x += offset_x
                        object.rect.y += offset_y

                # Check if level passed
                level.update()
                if player.rect.colliderect(level.ending.rect) and not level.ending.locked:
                    self.game_is_running = False
                    self.update(m)

                # Check if player died
                if player.rect.top > self.SCREEN_SIZE[1] + 100:
                    if self.VERBOSE: print 'Gameplay stopped, returning to main menu'
                    return

                '''
                All game drawing
                '''

                # Draw sky
                screen.fill(pygame.Color('lightblue'))
                screen.blit(pygame.image.load('sun.png'), (50, 50))

                # Draw foreground items
                level.draw()
                player_group.draw(screen)

                # Draw health bar
                health_bar_size = 20
                health_bar_multiplier = 5
                health_bar_x = (screen_x / 2) - (health_bar_multiplier * 100)
                health_bar_y = screen_y - health_bar_size
                health_rect = pygame.Rect(health_bar_x, health_bar_y, health_bar_multiplier * player.health, health_bar_size)
                pygame.draw.rect(screen, pygame.Color('red'), health_rect, 0)

                # Update display
                pygame.display.flip()

                # Set frame rate
                clock.tick(self.FPS)

        if self.VERBOSE: print 'Gameplay stopped, returning to main menu'
        return
