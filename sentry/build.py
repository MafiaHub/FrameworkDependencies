assert __name__ == "__main__"

import os
import sys

# Make sure we got the archive folder
if not os.path.isdir("archive"):
    raise ValueError("missing_archive_directory")

# Create our destination folder
if not os.path.isdir("build"):
    os.mkdir("build")
    os.mkdir("build/bin")
    os.mkdir("build/lib")
    os.mkdir("build/include")
    if sys.platform == "darwin":
        os.mkdir("build/bin/darwin_x64")
        os.mkdir("build/lib/darwin_x64")
    elif sys.platform == "win32":
        os.mkdir("build/bin/win_32")
        os.mkdir("build/lib/win_32")
        os.mkdir("build/lib/win_32/Debug")
        os.mkdir("build/lib/win_32/Release")

# Jump inside the build folder
os.chdir("archive")

if sys.platform == "darwin":
    # Build universal binaries on MacOS
    arch = "x86_64"
    if os.uname().nodename == "MacBook-Pro-de-Enguerrand.local":
        arch = "arm64;x86_64"
    os.system('cmake -B defaultbuild -DCMAKE_OSX_ARCHITECTURES="{}" -DSENTRY_BACKEND=crashpad -DBUILD_SHARED_LIBS=OFF'.format(arch))
    os.system('cmake --build defaultbuild --parallel')

    # Copy the built files to the destination folder
    os.system('cp defaultbuild/crashpad_build/client/libcrashpad_client.a ../build/lib/darwin_x64/.')
    os.system('cp defaultbuild/crashpad_build/handler/libcrashpad_handler_lib.a ../build/lib/darwin_x64/.')
    os.system('cp defaultbuild/crashpad_build/minidump/libcrashpad_minidump.a ../build/lib/darwin_x64/.')
    os.system('cp defaultbuild/crashpad_build/snapshot/libcrashpad_snapshot.a ../build/lib/darwin_x64/.')
    os.system('cp defaultbuild/crashpad_build/tools/libcrashpad_tools.a ../build/lib/darwin_x64/.')
    os.system('cp defaultbuild/crashpad_build/util/libcrashpad_util.a ../build/lib/darwin_x64/.')
    os.system('cp defaultbuild/libsentry.a ../build/lib/darwin_x64/.')

    # Copy the include
    os.system('cp include/sentry.h ../build/include/.')

    # Copy the binary
    os.system('cp defaultbuild/crashpad_build/handler/crashpad_handler ../build/bin/darwin_x64/.')

elif sys.platform == "win32":
    for mode in ['Debug', 'Release']:
        # Build on Windows
        os.system('cmake -B defaultbuild -DSENTRY_BACKEND=crashpad -DBUILD_SHARED_LIBS=OFF')

        if mode == "Release":
            os.system('cmake --build defaultbuild --parallel --config Release')
        else:
            os.system('cmake --build defaultbuild --parallel')

        # Copy the built files to the destination folder
        os.system('cp defaultbuild/crashpad_build/client/{}/libcrashpad_client.lib ../build/lib/win_32/.'.format(mode))
        os.system('cp defaultbuild/crashpad_build/handler/{}/libcrashpad_handler_lib.lib ../build/lib/win_32/.'.format(mode))
        os.system('cp defaultbuild/crashpad_build/minidump/{}/libcrashpad_minidump.lib ../build/lib/win_32/.'.format(mode))
        os.system('cp defaultbuild/crashpad_build/snapshot/{}/libcrashpad_snapshot.lib ../build/lib/win_32/.'.format(mode))
        os.system('cp defaultbuild/crashpad_build/tools/{}/libcrashpad_tools.lib ../build/lib/win_32/.'.format(mode))
        os.system('cp defaultbuild/crashpad_build/util/{}/libcrashpad_util.lib ../build/lib/win_32/.'.format(mode))
        os.system('cp defaultbuild/{}/sentry.lib ../build/lib/win_32/.'.format(mode))

        # Copy the include
        os.system('cp include/sentry.h ../build/include/.')

        # Copy the binary
        os.system('cp defaultbuild/crashpad_build/handler/{}/crashpad_handler.exe ../build/bin/win_32/.'.format(mode))
else:
    # Build on Linux
    # TODO: implement
    pass