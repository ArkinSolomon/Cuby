from distutils.core import setup
from glob import glob
import py2exe

data_files = [('images', glob('images/*.*')), ('audio', glob('audio/*.*')), ('levels', glob('levels/*.*'))]
setup(console=['__main__.py'], data_files=data_files, name='Cuby', icon_resources=[(0, 'images/icon.ico')])
