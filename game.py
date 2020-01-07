import pygame
import sys
from player import Player
from game_platform import Platform
from cloud import Cloud
import __main__ as m
from itertools import islice

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
        self.FPS = 800 # I don't know about this number but it's good (I think the framerate may be locked on this computer)
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

                # Loop through all horizontal collisions
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

                # Bound to walls
                if player.rect.left < horizontal_constraints[0]:
                    player.rect.left = horizontal_constraints[0]
                if player.rect.right > horizontal_constraints[1]:
                    player.rect.right = horizontal_constraints[1]

                # Vertical logic
                if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and not player.is_in_air:
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
                if player.vertical_acceleration != 0:
                    player.is_in_air = True

                # Change player image depending on direcion moved
                if player.prev_x < player.rect.x:
                    player.image = pygame.image.load('player.png')
                elif player.prev_x > player.rect.x:
                    player.image = pygame.image.load('player_reversed.png')

                # Stop or start rendering
                if keys[pygame.K_o] and self.DEBUG:
                    level.start_render()
                if keys[pygame.K_p] and self.DEBUG:
                    level.stop_render()

                # Move enemies
                for enemy in level.enemies:
                    is_x_collide = False
                    is_y_collide = False
                    add = enemy.speed
                    enemy.prev_x = enemy.rect.x
                    if enemy.rect.centerx < player.rect.centerx:
                        if enemy.rect.centerx + enemy.speed > player.rect.centerx:
                            add = player.rect.centerx - enemy.rect.centerx
                        enemy.rect.x += abs(add)
                    elif enemy.rect.centerx > player.rect.centerx:
                        if enemy.rect.centerx - enemy.speed < player.rect.centerx:
                            add = player.rect.centerx - enemy.rect.centerx
                        enemy.rect.x -= abs(add)
                    if enemy.rect.left < horizontal_constraints[0]:
                        enemy.rect.left = horizontal_constraints[0]
                    if enemy.rect.right > horizontal_constraints[1]:
                        enemy.rect.right = horizontal_constraints[1]
                    if enemy.prev_x < enemy.rect.x:
                        enemy.image = pygame.image.load('enemy.png')
                    elif enemy.prev_x > enemy.rect.x:
                        enemy.image = pygame.image.load('enemy_reversed.png')
                    eCopy = level.enemies.copy()
                    eCopy.remove(enemy)
                    player_collisions = pygame.sprite.spritecollide(enemy, player_group, False)
                    if len(player_collisions) > 0: is_x_collide = True
                    collisions = pygame.sprite.spritecollide(enemy, level.level_group, False) + pygame.sprite.spritecollide(enemy, level.objects, False) + pygame.sprite.spritecollide(enemy, eCopy, False) + player_collisions
                    if len(collisions) != 0 and not enemy.is_in_air:
                        enemy.jump()
                        self.JUMP_ENEMY.play()
                    for collision in collisions:
                        if enemy.prev_x < enemy.rect.x:
                            enemy.rect.right = collision.rect.left
                        elif enemy.prev_x > enemy.rect.x:
                            enemy.rect.left = collision.rect.right
                    enemy.prev_y = enemy.rect.y
                    enemy.vertical_acceleration += self.GRAVITY
                    enemy.rect.y += enemy.vertical_acceleration
                    player_collisions = pygame.sprite.spritecollide(enemy, player_group, False)
                    c = True
                    if len(player_collisions) > 0:
                        is_y_collide = True
                        if player.rect.bottom < enemy.rect.centery and not enemy.is_in_air:
                            enemy.kill()
                            c = False
                    if not c: continue
                    for collision in pygame.sprite.spritecollide(enemy, level.level_group, False) + pygame.sprite.spritecollide(enemy, level.objects, False) + pygame.sprite.spritecollide(enemy, eCopy, False) + player_collisions:
                        if enemy.prev_y < collision.rect.top:
                            enemy.rect.bottom = collision.rect.top
                            enemy.is_in_air = False
                        else:
                            enemy.rect.top = collision.rect.bottom
                        enemy.vertical_acceleration = 0
                    if enemy.vertical_acceleration != 0:
                        enemy.is_in_air = True
                    if is_x_collide or is_y_collide: player.health -= 1
                    if enemy.rect.centery > vertical_constraints[1]:
                        enemy.kill()

                # Player kill
                if player.health <= 0:
                    player.kill
                    if self.VERBOSE: print 'Gameplay stopped, returning to main menu'
                    return

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
