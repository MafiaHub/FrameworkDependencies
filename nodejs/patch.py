import os
from distutils.dir_util import copy_tree

copy_tree('nodejs/patch/node', '../archive')
os.system("patch -p1 archive/node.gyp nodejs/patch/node.gyp.patch")
os.system("patch -p1 archive/tools/install.py nodejs/patch/install.py.patch")