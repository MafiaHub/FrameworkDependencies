assert __name__ == "__main__"

import urllib.request
import os
import sys
import zipfile

def process(version):
    # Download the file
    urllib.request.urlretrieve("https://github.com/getsentry/sentry-native/releases/download/{}/sentry-native.zip".format(version), "archive.zip")
    if not os.path.isfile("archive.zip"):
        raise ValueError("missing_archive_file")

    # Unzip the archive
    with zipfile.ZipFile("archive.zip", "r") as zip_ref:
        zip_ref.extractall("archive")

    # Delete the downloaded file
    os.remove("archive.zip")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError('missing_version_argument')
    process(sys.argv[1])