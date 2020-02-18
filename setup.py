from distutils.core import setup
from glob import glob
import py2exe

data_files = [('images', glob('images/*.*')), ('audio', glob('audio/*.*')), ('levels', glob('levels/*.*')), ('fonts', glob('fonts/*.*'))]
setup(console=['__main__.py'], data_files=data_files, name='Cuby')
