assert __name__ == "__main__"

import shutil
import sys

def archive(mode):
    zipBasename = 'nodejs-{}-{}'.format(sys.platform, mode)
    shutil.make_archive(zipBasename, 'zip', base_dir='build')
    print(zipBasename + '.zip')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError('missing_mode_argument')
    
    archive(sys.argv[1])