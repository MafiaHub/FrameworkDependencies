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

# Jump inside the build folder
os.chdir("archive")

if sys.platform == "darwin":
    # Build universal binaries on MacOS
    os.system('cmake -B defaultbuild -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64" -DSENTRY_BACKEND=crashpad -DBUILD_SHARED_LIBS=OFF')
    os.system('cmake --build defaultbuild --parallel')

    # Copy the built files to the destination folder
    os.system('cp defaultbuild/crashpad_build/client/libcrashpad_client.a ../build/lib/.')
    os.system('cp defaultbuild/crashpad_build/handler/libcrashpad_handler_lib.a ../build/lib/.')
    os.system('cp defaultbuild/crashpad_build/minidump/libcrashpad_minidump.a ../build/lib/.')
    os.system('cp defaultbuild/crashpad_build/snapshot/libcrashpad_snapshot.a ../build/lib/.')
    os.system('cp defaultbuild/crashpad_build/tools/libcrashpad_tools.a ../build/lib/.')
    os.system('cp defaultbuild/crashpad_build/util/libcrashpad_util.a ../build/lib/.')
    os.system('cp defaultbuild/libsentry.dylib ../build/lib/.')

    # Copy the include
    os.system('cp include/sentry.h ../build/include/.')

    # Copy the binary
    os.system('cp defaultbuild/crashpad_build/handler/crashpad_handler ../build/bin/.')

elif sys.platform == "win32":
    # Build on Window
    os.system('cmake -B defaultbuild -DSENTRY_BACKEND=crashpad -DBUILD_SHARED_LIBS=OFF')
    os.system('cmake --build defaultbuild --parallel')

    # Copy the built files to the destination folder
    os.system('cp defaultbuild/crashpad_build/client/Debug/libcrashpad_client.lib ../build/lib/.')
    os.system('cp defaultbuild/crashpad_build/handler/Debug/libcrashpad_handler_lib.lib ../build/lib/.')
    os.system('cp defaultbuild/crashpad_build/minidump/Debug/libcrashpad_minidump.lib ../build/lib/.')
    os.system('cp defaultbuild/crashpad_build/snapshot/Debug/libcrashpad_snapshot.lib ../build/lib/.')
    os.system('cp defaultbuild/crashpad_build/tools/Debug/libcrashpad_tools.lib ../build/lib/.')
    os.system('cp defaultbuild/crashpad_build/util/Debug/libcrashpad_util.lib ../build/lib/.')
    os.system('cp defaultbuild/Debug/sentry.lib ../build/lib/.')

    # Copy the include
    os.system('cp include/sentry.h ../build/include/.')

    # Copy the binary
    os.system('cp defaultbuild/crashpad_build/handler/Debug/crashpad_handler.exe ../build/bin/.')
else:
    # Build on Linux
    # TODO: implement
    pass