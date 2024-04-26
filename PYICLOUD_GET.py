from __future__ import print_function
import click
import os
import sys
import socket
import requests
import time
from tqdm import tqdm
from dateutil.parser import parse
from pyicloud import PyiCloudService
import numpy as np
import asyncio
import aiomultiprocess
import shutil

# For retrying connection after timeouts and errors
MAX_RETRIES = 5
WAIT_SECONDS = 5

def cycle_files():
    directoryA = "PhotosA/"
    directoryB = "PhotosB/"
    if len(os.listdir(directoryA)) > 0:
        # try:
        filesB = os.listdir(directoryB)
        for file in filesB:
            file_pathB = os.path.join(directoryB, file)
            try:
                shutil.rmtree(file_pathB)
            except:
                "Error"
        filesA = os.listdir(directoryA)
        for file in filesA:
            file_pathA = os.path.join(directoryA, file)
            file_pathB = os.path.join(directoryB, file)
            os.rename(file_pathA, file_pathB)

def download(directory = os.getcwd() + "/PhotosA", username = "olivine8910@gmail.com", password = "sadnav-diqtyf-boQni1", size = "original", download_videos = 0, force_size = 0):
    """Download/Refresh 50 iCloud photos from favorites to a local directory"""
    icloud = authenticate(username, password)

    print("Looking up all photos...")
    #all_photos = icloud.photos.all
    all_photos = icloud.photos.albums['Favorites'] #only download from favorites
    photos_count = 200
    p = np.random.permutation(len(list(all_photos)))
    random_file_list = [list(all_photos)[i] for i in p[0:photos_count]]

    directory = directory.rstrip('/')

    if download_videos:
        print("Downloading %d %s photos and videos to %s/ ..." % (photos_count, size, directory))
    else:
        print("Downloading %d %s photos to %s/ ..." % (photos_count, size, directory))

    pbar = tqdm(random_file_list, total=photos_count) # limit number of downloads to 50

    for photo in pbar:
        for i in range(MAX_RETRIES):
            try:
                if not download_videos and not photo.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.HEIC', '.tiff', '.tif', '.raw', '.arw', '.dng')):
                    pbar.set_description("Skipping %s, only downloading photos." % photo.filename)
                    continue
                
                date_path = ""
                created_date = photo.created
                if isinstance(created_date, str):
                    created_date = parse(photo.created)
                date_path = '{:%Y/%m/%d}'.format(created_date)
                download_dir = '/'.join((directory, date_path))

                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)

                download_photo(photo, size, force_size, download_dir, pbar)
                break

            except (requests.exceptions.ConnectionError, socket.timeout):
                tqdm.write('Connection failed, retrying after %d seconds...' % WAIT_SECONDS)
                time.sleep(WAIT_SECONDS)

        else:
            tqdm.write("Could not process %s! Maybe try again later." % photo.filename)

    print("All photos have been downloaded!")

def authenticate(username, password):
    print("Signing in...")

    api = PyiCloudService(username, password)

    if api.requires_2fa:
        print("Two-factor authentication required.")
        code = input("Enter the code you received of one of your approved devices: ")
        result = api.validate_2fa_code(code)
        print("Code validation result: %s" % result)

        if not result:
            print("Failed to verify security code")
            sys.exit(1)

        if not api.is_trusted_session:
            print("Session is not trusted. Requesting trust...")
            result = api.trust_session()
            print("Session trust result %s" % result)

            if not result:
                print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
    elif api.requires_2sa:
        import click
        print("Two-step authentication required. Your trusted devices are:")

        devices = api.trusted_devices
        for i, device in enumerate(devices):
            print(
                "  %s: %s" % (i, device.get('deviceName',
                "SMS to %s" % device.get('phoneNumber')))
            )

        device = click.prompt('Which device would you like to use?', default=0)
        device = devices[device]
        if not api.send_verification_code(device):
            print("Failed to send verification code")
            sys.exit(1)

        code = click.prompt('Please enter validation code')
        if not api.validate_verification_code(device, code):
            print("Failed to verify verification code")
            sys.exit(1)

    return api

def truncate_middle(s, n):
    if len(s) <= n:
        return s
    n_2 = int(n) / 2 - 2
    n_1 = n - n_2 - 4
    if n_2 < 1: n_2 = 1
    return u'{0}...{1}'.format(s[:int(n_1)], s[-int(n_2):])

def download_photo(photo, size, force_size, download_dir, pbar):
    filename_with_size = photo.filename.replace('.', '-%s.' % size)
    download_path = '/'.join((download_dir, filename_with_size))

    truncated_filename = truncate_middle(filename_with_size, 24)
    truncated_path = truncate_middle(download_path, 72)

    if os.path.isfile(download_path):
        pbar.set_description("%s already exists." % truncated_path)
        return

    # Fall back to original if requested size is not available
    if size not in photo.versions and not force_size and size != 'original':
        download_photo(photo, 'original', True, download_dir, pbar)
        return

    pbar.set_description("Downloading %s to %s" % (truncated_filename, truncated_path))

    for i in range(MAX_RETRIES):
        try:
            download = photo.download(size)

            if download:
                with open(download_path, 'wb') as file:
                    for chunk in download.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
            else:
                tqdm.write("Could not find URL to download %s for size %s!" % (photo.filename, size))

            return

        except (requests.exceptions.ConnectionError, socket.timeout):
            tqdm.write('%s download failed, retrying after %d seconds...' % (photo.filename, WAIT_SECONDS))
            time.sleep(WAIT_SECONDS)
    else:
        tqdm.write("Could not download %s! Maybe try again later." % photo.filename)

# if __name__ == '__main__':
#     download()