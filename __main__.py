import sys
from game import Game
import levels as l
import json
import os
from os.path import exists, isfile, isdir
from pathlib import Path
import pygame
from button import Button

'''
This file handles the game initialization as well as game saving.
'''

os.system('clear')

# Runtime flags
VERBOSE = True if '-v' in sys.argv or '--verbose' in sys.argv else False
if VERBOSE: print 'Running The Legend of Cube in verbose mode'
level_override = None
if '-l' in sys.argv or '--level' in sys.argv:
    if '-l' in sys.argv:
        level_override = int(sys.argv[sys.argv.index('-l') + 1])
    else:
        level_override = int(sys.argv[sys.argv.index('-l') + 1])
DEBUG = True if '-d' in sys.argv or '--debug' in sys.argv else False
if DEBUG: print 'Debugging The Legend of Cube mode'

# Update level in file
def __update_level_file(c):
        with __DATA_PATH.open(mode='w') as file:
            file.write(unicode('{"currentLevel":%d}' % c))

# Set the level in the file to 0
def __reset_level_file():
    __update_level_file(0)

# Insert levels here
__LEVELS = [l.Level1, l.Level2, l.Level3, l.Level4]

current_level = 0

# Find current level of user
__DATA_FILE_NAME = 'data.json'
__DATA_FOLDER = Path('data')
__DATA_PATH = Path('%s/%s' % (__DATA_FOLDER.name, __DATA_FILE_NAME))
__new_file = False
__file_exists = __DATA_FOLDER.exists() and __DATA_FOLDER.is_dir() and __DATA_PATH.exists() and __DATA_PATH.is_file()
if not __file_exists:
    if VERBOSE: print 'Save file doesn\'t exist, making new'
    if not exists(__DATA_FOLDER.name) and not isdir(__DATA_FOLDER.name):
        os.mkdir(__DATA_FOLDER.name)
    __DATA_PATH.touch()
    __new_file = True
if not __new_file:
    if VERBOSE: print 'Save file exists, loading data'
    with __DATA_PATH.open(mode='r') as f:
        file = f.readline()
        try:
            parsed_data = json.loads(file)

            # Check if game is completed
            if parsed_data['currentLevel'] == len(__LEVELS):
                current_level = 0
            else:
                current_level = parsed_data['currentLevel']
            __update_level_file(current_level)
        except Exception as e:
            __reset_level_file()
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

# Main menu
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('The Legend of Cube')
pygame.mixer.music.load('CubeMusic.wav')
pygame.mixer.music.play(-1)

screen_x, screen_y = pygame.display.get_surface().get_size()
button_width = screen_x * .33
button_height = screen_y * .1

start_button = Button([(screen_x / 2) - button_width / 2, (screen_y / 2) - button_height / 2], button_width, button_height, 'Start', 50, screen)
quit_button = Button([90, screen_y - 190], 100, 100, 'Quit', 38, screen)

main_menu_is_active = True

def __quit():
    main_menu_is_active = False
    pygame.quit()
    sys.exit(0)

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
            if VERBOSE: print 'Starting game at level %d' % (current_level + 1)
            Game(__LEVELS, update, VERBOSE, DEBUG).start(screen)

        if quit_button.check_click(mouse_pos[0], mouse_pos[1]):
            if VERBOSE: print 'Game quitting'
            __quit()

    screen.fill(pygame.Color('lightblue'))
    start_button.draw()
    quit_button.draw()
    pygame.display.flip()
