assert __name__ == "__main__"

import os
import sys
import subprocess

flags = ['--with-intl=small-icu']
additionalDebugFlags = ['--debug-nghttp2', '--debug-lib']

def process(mode):
    # Prepare the build flags
    if mode == "Debug":
        flags = flags + additionalDebugFlags

    # Make sure we got the archive folder
    if not os.path.isdir("archive"):
        raise ValueError("missing_archive_directory")

    # Create our destination folder
    if not os.path.isdir("build"):
        os.mkdir("build")
        os.mkdir("build/{}".format(mode))

    # Jump inside the build folder
    os.chdir("archive")

    if sys.platform == "darwin":
        if mode == "Debug":
            subprocess.check_call([ sys.executable, 'configure.py', '--ninja', '--debug' ] + flags)
            subprocess.check_call(['ninja', '-C', 'out/Debug'])
        elif mode == "Release":
            subprocess.check_call([ sys.executable, 'configure.py', '--ninja' ] + flags)
            subprocess.check_call(['ninja', '-C', 'out/Release'])
    if sys.platform == "win32":
        env = os.environ.copy()
        env['config_flags'] = ' '.join(flags)
        if mode == "Debug":
            subprocess.check_call(
                ['cmd', '/c', 'vcbuild.bat', 'debug', 'debug-nghttp2', 'x86', 'small-icu'],
                env=env
            )
        elif mode == "Release":
            subprocess.check_call(
                ['cmd', '/c', 'vcbuild.bat', 'release', 'x86', 'small-icu'],
                env=env
            )
for mode in ['Debug', 'Release']:
    process(mode)