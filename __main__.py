import sys
from game import Game
from level_creator import Level_Creator
from level import Level
from game_platform import Platform
from movable_object import Movable_Object
from ending import Ending
from enemy import Enemy
from cloud import Cloud
import json
import os
from os.path import exists, isfile, isdir
from pathlib import Path
import pygame
from button import Button

'''
This file handles the game initialization as well as game saving.
'''

VERSION = '0.3.1'

# Clear console
if sys.platform == 'win32':
    os.system('cls')
else:
    os.system('clear')

# Runtime flags
VERBOSE = True if '-v' in sys.argv or '--verbose' in sys.argv else False
if VERBOSE: print 'Running Cuby in verbose mode'
level_override = None
if '-l' in sys.argv or '--level' in sys.argv:
    if '-l' in sys.argv:
        level_override = int(sys.argv[sys.argv.index('-l') + 1])
    else:
        level_override = int(sys.argv[sys.argv.index('-l') + 1])
DEBUG = True if '-d' in sys.argv or '--debug' in sys.argv else False
if DEBUG: print 'Debugging Cuby'
SHOW_FPS = True if '-f' in sys.argv or '--show-fps' in sys.argv else False
if VERBOSE and SHOW_FPS: print 'Showing FPS in-game'
NOAI = True if '--no-ai' in sys.argv else False
if NOAI: print 'Starting game with enemy AI disabled'
NOAUDIO = True if '--no-audio' in sys.argv else False
if NOAUDIO: print 'Starting game with audio disabled'

'''
Initialization
'''

if VERBOSE: print 'Initializing Cuby version %s' % VERSION

pygame.init()
if VERBOSE: print 'Pygame initialized'
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE)

# Load images
LOGO = pygame.image.load('images/logo.png')
SUN = pygame.image.load('images/sun.png')

# Update level in file
def __update_level_file(c):
        with __data_path.open(mode='w') as file:
            file.write(unicode('{"currentLevel":%d}' % c))

# Set the level in the file to 0
def __reset_level_file(): __update_level_file(0)

# Level parsing
__levels = []
def parse_levels():

    # Chaeck if the level file exists
    __level_file_name = 'levels.lvl'
    __level_folder = Path('levels')
    __level_path = Path('%s/%s' % (__level_folder.name, __level_file_name))
    __new_file = False
    __file_exists = __level_folder.exists() and __level_folder.is_dir() and __level_path.exists() and __level_path.is_file()
    if not __file_exists:
        if VERBOSE: print 'Level file doesn\'t exist, making new'
        if not exists(__level_folder.name) and not isdir(__level_folder.name):
            os.mkdir(__level_folder.name)
        __level_path.touch()
        __new_file = True

    if not __new_file:
        if VERBOSE: print 'Level file exists'
        with __level_path.open(mode='r') as f:
            file = str(f.read())
            levels = file.split('*LEVEL*\n')
            del levels[0]
            for l in levels:
                if VERBOSE: 'Parsing new level'
                lines = l.split('\n')
                del lines[len(lines) - 1]
                level = Level(screen, NOAUDIO)

                # Loop through all lines
                for line in lines:
                    if VERBOSE: print 'Parsing line: %s' % line
                    item = line.split('$')
                    coords = json.loads('{"d":' + item[1] + '}')['d']
                    if item[0] == 'PLA':
                        level.add_platform(Platform(coords, int(item[2]), int(item[3]), pygame.Color(item[4]), screen))
                    elif item[0] == 'PLS':
                        level.player_start = coords
                    elif item[0] == 'ENE':
                        level.enemies.add(Enemy(coords, screen))
                    elif item[0] == 'OBJ':
                        level.add_object(Movable_Object(coords))
                    elif item[0] == 'END':
                        level.set_ending(Ending(coords, screen))
                level.calc_max_values()
                __levels.append(level)

# Find current level of user
current_level = 0
__data_file_name = 'data.json'
__data_folder = Path('data')
__data_path = Path('%s/%s' % (__data_folder.name, __data_file_name))
__new_file = False

# Check if the data file exists
__file_exists = __data_folder.exists() and __data_folder.is_dir() and __data_path.exists() and __data_path.is_file()
if not __file_exists:
    if VERBOSE: print 'Save file doesn\'t exist, making new'
    if not exists(__data_folder.name) and not isdir(__data_folder.name):
        os.mkdir(__data_folder.name)
    __data_path.touch()
    __new_file = True
if not __new_file:
    if VERBOSE: print 'Save file exists, loading data'
    with __data_path.open(mode='r') as f:
        file = f.readline()
        try:
            parsed_data = json.loads(file)

            # Check if game is completed
            if parsed_data['currentLevel'] == len(__levels):
                current_level = 0
            else:
                current_level = parsed_data['currentLevel']
            __update_level_file(current_level)
        except Exception as e: __reset_level_file()
else:
    if VERBOSE: print 'Save file doesn\'t exist, making new'
    __reset_level_file()

if level_override != None:
    print 'Level file overriden, starting save file at %d' % (level_override + 1)
    current_level = level_override
    __update_level_file(level_override)

# This runs on every level pass
def update(m):
    if VERBOSE: print 'Level %d passed' % (m.current_level + 1)
    m.current_level += 1
    __update_level_file(m.current_level)

'''
Main menu
'''
pygame.display.set_caption('Cuby %s' % VERSION)
if not NOAUDIO:
    pygame.mixer.music.load('audio/cube_music.wav')
    pygame.mixer.music.play(-1)

# Button setup
screen_x, screen_y = pygame.display.get_surface().get_size()
button_width = screen_x * .33
button_height = screen_y * .1

# Menu buttons
start_button = Button([(screen_x / 2) - button_width / 2, ((screen_y / 2) - button_height / 2) - (button_height / 2) - 15], button_width, button_height, 'Start', 50, screen)
level_create_button = Button([(screen_x / 2) - button_width / 2, ((screen_y / 2) - button_height / 2) + (button_height / 2) + 15], button_width, button_height, 'Level creator', 50, screen)
quit_button = Button([90, screen_y - 190], 100, 100, 'Quit', 38, screen)
clouds = Cloud(screen, screen_x, screen_y, [-150, screen_x + 150], [-450, screen_y + 450], False).clouds
clouds_2 = Cloud(screen, screen_x, screen_y, [-150 + screen_x, 2 * screen_x + 150], [-450, screen_y + 450], False).clouds

main_menu_is_active = True

def __quit():
    main_menu_is_active = False
    pygame.quit()
    sys.exit(0)

cloud_counter = 0
clock = pygame.time.Clock()

# Font things
fps_font = pygame.font.Font('fonts/FreeSansBold.ttf', 20)
version_font = pygame.font.SysFont('Comic Sans MS', 16)
version_data = 'Cuby %s' % VERSION
version_size = version_font.size(version_data)

parse_levels()
start_button.disabled = len(__levels) == 0
while main_menu_is_active:

    for event in pygame.event.get():

        # If user quits
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            __quit()

    mouse_pos = pygame.mouse.get_pos()

    # Buttons
    if pygame.mouse.get_pressed()[0]:

        # Start the game
        if start_button.check_click(mouse_pos[0], mouse_pos[1]):
            if current_level >= len(__levels):
                current_level = 0
                if VERBOSE: print 'Currrent level higher than max levels, reseting to 0'
            if VERBOSE: print 'Starting game at level %d' % (current_level + 1)
            Game(__levels, update, VERBOSE, DEBUG, NOAI, NOAUDIO, SHOW_FPS).start(screen)
            pygame.mouse.set_visible(True)
            __levels = []
            parse_levels()

        if level_create_button.check_click(mouse_pos[0], mouse_pos[1]):
            if VERBOSE: print 'Starting level creator'
            Level_Creator(VERBOSE, SHOW_FPS).start(screen)
            __levels = []
            parse_levels()

        # Quit the game
        if quit_button.check_click(mouse_pos[0], mouse_pos[1]):
            if VERBOSE: print 'Game quitting'
            __quit()

    screen.fill(pygame.Color('lightblue'))
    screen.blit(SUN, (50, 50))

    clouds.draw(screen)
    clouds_2.draw(screen)
    least_cloud = 0
    for cloud in clouds:
        if cloud.rect.right > least_cloud: least_cloud = cloud.rect.right
        cloud.rect.right -= screen_x * 5e-6
    for cloud in clouds_2: cloud.rect.right -= 5e-6
    if least_cloud <= 0:
        clouds = clouds_2
        clouds_2 = Cloud(screen, screen_x, screen_y, [-150 + screen_x, 2 * screen_x + 150], [-450, screen_y + 450], False).clouds

    version_text = version_font.render(version_data, True, (0, 0, 0))
    screen.blit(version_text, (screen_x - version_size[0] - 10, screen_y - version_size[1] - 10))

    screen.blit(LOGO, ((screen_x / 2) - 450, 60))
    start_button.draw()
    quit_button.draw()
    level_create_button.draw()

    if SHOW_FPS: screen.blit(fps_font.render(str(int(clock.get_fps())), True, pygame.Color('white'), pygame.Color('black')), (0, 0))

    pygame.display.flip()

    clock.tick(60)
