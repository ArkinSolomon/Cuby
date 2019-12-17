import sys
from game import Game
import levels as l
import json
import os
from os.path import exists, isfile, isdir
from pathlib import Path

'''
This file handles the game initialization as well as game saving.
'''

os.system('clear')

# Run time flags
VERBOSE = True if '-v' in sys.argv or '--verbose' in sys.argv else False
if VERBOSE: print 'Running The Legend of Cube in verbose mode'
level_override = None
if '-l' in sys.argv or '--level' in sys.argv:
    if '-l' in sys.argv:
        level_override = int(sys.argv[sys.argv.index('-l') + 1])
    else:
        level_override = int(sys.argv[sys.argv.index('-l') + 1])

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

# Start the game
if VERBOSE: print 'Starting game at level %d' % (current_level + 1)
Game(__LEVELS, update, VERBOSE).start()
