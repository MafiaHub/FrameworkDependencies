assert __name__ == "__main__"

import urllib.request
import os
import sys
import tarfile

def process(version):
    # Download the file
    urllib.request.urlretrieve("https://nodejs.org/dist/v{}/node-v{}.tar.gz".format(version, version), "archive.tar.gz", ssl=False)
    if not os.path.isfile("archive.tar.gz"):
        raise ValueError("missing_archive_file")

    # Unzip the archive
    with tarfile.open("archive.tar.gz", "r") as zip_ref:
        zip_ref.extractall("archive")

    # Delete the downloaded file
    os.remove("archive.tar.gz")

    # Move the inner content
    os.system("mv archive/node-v{}/* archive/.".format(version))
    os.system("rm -rf archive/node-v{}".format(version))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError('missing_version_argument')
    process(sys.argv[1])
