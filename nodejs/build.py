assert __name__ == "__main__"

from genericpath import isdir
import os
import sys
import subprocess
import shutil
import glob

flags = ['--with-intl=small-icu']
additionalDebugFlags = ['--debug-nghttp2', '--debug-lib']
buildModes = ['Debug', 'Release']

nodeSrcFolder = "archive"
resultFolder = "build"

def build(mode):
    global flags
    # Prepare the build flags
    if mode == "Debug":
        flags = flags + additionalDebugFlags

    # Make sure we got the archive folder
    if not os.path.isdir("archive"):
        raise ValueError("missing_archive_directory")

    # Jump inside the build folder
    os.chdir("archive")

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
    else:
        if mode == "Debug":
            subprocess.check_call([ sys.executable, 'configure.py', '--ninja', '--debug' ] + flags)
            subprocess.check_call(['ninja', '-C', 'out/Debug'])
        elif mode == "Release":
            subprocess.check_call([ sys.executable, 'configure.py', '--ninja' ] + flags)
            subprocess.check_call(['ninja', '-C', 'out/Release'])
    

    # Get back to previous directory
    os.chdir("..")

def postproc(mode):
    global nodeSrcFolder

    # Prepare the destination folder for each mode
    destinationLibPath = "build/{}/lib".format(mode)
    destinationIncludePath = "build/{}/include".format(mode)
    destinationDepsPath = "build/{}/deps".format(mode)
    if not os.path.isdir(destinationLibPath):
        os.makedirs(destinationLibPath, exist_ok=True)

    # Copy libraries and strip them
    if sys.platform == 'win32':
        for libFile in os.scandir(nodeSrcFolder + '\\out\\' + mode + '\\lib'):
            if libFile.is_file() and (libFile.name.endswith('.lib') or libFile.name.endswith('.dll')):
                print('Copying', libFile.name)
                shutil.copy(libFile.path, destinationLibPath)
    elif sys.platform == 'darwin':
        for libFile in os.scandir(nodeSrcFolder + '/out/' + mode):
            if libFile.is_file() and (libFile.name.endswith('.a') or libFile.name.endswith('.dylib')):
                print('Copying {} ({}) to {}'.format(libFile.name, libFile.path, destinationLibPath))
                shutil.copy(libFile.path, destinationLibPath)
                print('Striping', libFile.name)
                subprocess.check_call(['strip', '-x', os.path.join(destinationLibPath, libFile.name)])
    elif sys.platform == 'linux':
        for dirname, _, basenames in os.walk(nodeSrcFolder + '/out/' + mode + '/obj'):
            for basename in basenames:
                if (basename.endswith('.a') or basename.endswith('.so')) and filterLibFile(basename):
                    subprocess.run(
                        'ar -t {} | xargs ar rs {}'.format(
                            os.path.join(dirname, basename),
                            os.path.join(destinationLibPath, basename)
                        ),
                        check=True, shell=True
                    )

    additional_obj_glob = nodeSrcFolder + '/out/' + mode + '/obj/src/node_mksnapshot.*.o'
    if sys.platform == 'win32':
        additional_obj_glob = nodeSrcFolder + '/out/' + mode + '/obj/node_mksnapshot/src/*.obj'

    if sys.platform == 'win32':
        subprocess.check_call([
                'lib', '/OUT:' + os.path.join(destinationLibPath, "libnode_snapshot.lib")
            ] + 
            glob.glob(additional_obj_glob) + 
            glob.glob(nodeSrcFolder + '/out/' + mode + '/obj/node_mksnapshot/tools/msvs/pch/*.obj')
        )
    else:
        subprocess.check_call([
            'ar', 'cr', 
            os.path.join(destinationLibPath, "libnode_snapshot.a")
        ] + glob.glob(additional_obj_glob))

    # Copy the include and deps
    shutil.copytree(os.path.join(nodeSrcFolder, 'include'), destinationIncludePath)
    shutil.copytree(os.path.join(nodeSrcFolder, 'deps'), destinationDepsPath)

# Call the build method to build both debug and release workflows            
for mode in buildModes:
    build(mode)

# Copy the headers
env = os.environ.copy()
env['HEADERS_ONLY'] = '1'
os.chdir("archive")
subprocess.check_call([ sys.executable, 'tools/install.py', 'install', '.', '' ], env=env)

# Get back to our root folder
os.chdir("..")
if not os.path.isdir("build"):
    os.mkdir("build")

# Do the post processing
for mode in buildModes:
    postproc(mode)