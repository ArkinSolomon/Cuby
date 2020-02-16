# Cuby

## About:

Cuby is a game in where you, a cube, must defeat all the evil circles with poisonous skin by crushing them. This game was created for my Introduction to Computer Programming class and is very much still in development.

## Installation:

Compiled exe files will be found under the 'releases' tab in GitHub. Unzip the folder and run `Cuby.exe`. You may need to [download and install Microsoft's Visual C++](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads). It can also be run directly from the command line by downloading the source using Python 2.7. Running it from the command line provides additional command line arguments, `-v` or `--verbose` prints verbose output. `-d` or `--debug` enables debug keys (found below). `-f` or `--show-fps` shows the current game fps in the top-left corner of the screen. `-l <level>` or `--level <level>` forces the game to start from a specific level. `--no-ai` starts the game and does not enable enemy AI (It can be enabled using debug keys). `--no-audio` does not enable audio. 
You will need these modules if you run it using Python:
- Pygame
- Pathlib

If you want to compile it from source you will need to install [py2exe for Python 2.7](https://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/). Depending on your Python installation, you may need to download the unofficial version from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/).

## Debug keys:

- o: Enable rendering checking
- p: Disable rendering checking
- MINUS: Disable enemy AI
- EQUALS: Enable enemy AI
- F1: Enable free camera movement
- F2: Disable free camera movement
