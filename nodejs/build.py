import os
import sys
import shutil
import subprocess

archiveFolder = "archive"
resultFolder = "build"

def build(mode):
    try:
        # Make sure we got the archive folder
        if not os.path.isdir("archive"):
            raise ValueError("missing_archive_directory")

        # Jump inside the build folder
        os.chdir("archive")

        if sys.platform == "win32":
            if mode == "Debug":
                subprocess.check_call(['cmd', '/c', 'vcbuild.bat', 'x64', 'debug', 'dll', 'vs2019', 'no-cctest'])
            else:
                subprocess.check_call(['cmd', '/c', 'vcbuild.bat', 'x64', 'release', 'dll', 'vs2019', 'no-cctest'])
        else:
            subprocess.check_call([sys.executable, 'configure.py', '--shared'])
            subprocess.check_call(['make', '-j4'])

        # Generate the includes
        env = os.environ.copy()
        subprocess.check_call([ sys.executable, 'tools/install.py', 'install', '.', '' ], env=env)

        # Get back to previous directory
        os.chdir("..")

        return True
    except:
        return False

def postproc(mode):
    # Prepare the destination folder for each mode
    destinationPath = "{}/{}".format(resultFolder, mode)

    # Copy the release folder
    shutil.copytree(os.path.join(archiveFolder, 'usr', 'local'), destinationPath)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError('missing_mode_argument')
    if build(sys.argv[1]):
       postproc(sys.argv[1])
