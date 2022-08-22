assert __name__ == "__main__"

import urllib.request
import os
import zipfile

# Download the file
# TODO: get input for the version
urllib.request.urlretrieve("https://github.com/getsentry/sentry-native/releases/download/0.5.0/sentry-native.zip", "archive.zip")
if not os.path.isfile("archive.zip"):
    raise ValueError("missing_archive_file")

# Unzip the archive
with zipfile.ZipFile("archive.zip", "r") as zip_ref:
    zip_ref.extractall("archive")

# Delete the downloaded file
os.remove("archive.zip")