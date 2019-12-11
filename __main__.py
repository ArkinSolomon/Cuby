from game import Game
import levels as l
import json
import os
from os.path import exists, isfile, isdir
from pathlib import Path

'''
This file handles the game initialization as well as game saving.
'''

# Insert levels here
__LEVELS = [l.Level1, l.Level2]

current_level = 0

# Update level in file
def __update_level_file(c):
        with __DATA_PATH.open(mode='w') as file:
            file.write(unicode('{"currentLevel":%d}' % c))

# Set the level inthe file to 0
def __reset_level_file():
    __update_level_file(0)

# Find current level of user
__DATA_FILE_NAME = 'data.json'
__DATA_FOLDER = Path('data')
__DATA_PATH = Path('%s/%s' % (__DATA_FOLDER.name, __DATA_FILE_NAME))
__new_file = False
__file_exists = __DATA_FOLDER.exists() and __DATA_FOLDER.is_dir() and __DATA_PATH.exists() and __DATA_PATH.is_file()
if not __file_exists:
    if not exists(__DATA_FOLDER.name) and not isdir(__DATA_FOLDER.name):
        os.mkdir(__DATA_FOLDER.name)
    __DATA_PATH.touch()
    __new_file = True
if not __new_file:
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
    __reset_level_file()

# This runs on every level pass
def update(m):
    m.current_level += 1
    __update_level_file(m.current_level)

# Start the game
Game(__LEVELS, update).start()
