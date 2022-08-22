assert __name__ == "__main__"

import shutil
import sys

zipBasename = 'sentry-{}'.format(sys.platform)

shutil.make_archive(zipBasename, 'zip', base_dir='build')

print(zipBasename + '.zip')