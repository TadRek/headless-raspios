#!/usr/bin/python3

from urllib.request import urlretrieve
from os import path, mkdir, mknod, system, listdir
from zipfile import ZipFile
from shutil import rmtree
from getpass import getpass

DOWNLOAD_URL = 'https://downloads.raspberrypi.org/raspios_lite_armhf_latest'
DIR = path.dirname(path.abspath(__file__))
TMP = DIR + '/tmp/'
BOOT = TMP + 'boot/'
SD = '/dev/mmcblk0'


def main():
    create_tmp_dir()
    download_image()
    unzip()
    sd_card()
    mount_boot_partition()
    enable_ssh()
    enable_wifi()
    cleanup()


def create_tmp_dir():
    if path.isdir(TMP):
        print('Tmp folder exist, exiting')
    else:
        print('Creating tmp folder')
        mkdir(TMP)


def download_image():
    print('Downloading latest RaspiOS image')
    urlretrieve(DOWNLOAD_URL, TMP + 'raspios.zip')


def unzip():
    print('Extracting image')

    with ZipFile(TMP + 'raspios.zip', 'r') as myzip:
        myzip.extractall(TMP) 


def sd_card(): 
    ISO= [_ for _ in listdir(TMP) if _.endswith('.img')]
    print('Copying files to SD card')
    system(f'sudo dd bs=4M if={TMP}{ISO[0]} of={SD} conv=fsync')


def mount_boot_partition():
    print('Creating boot partition mounting directory')
    mkdir(BOOT)
    print(f'Mounting boot partition to {BOOT}')
    system(f'sudo mount {SD}p1 {BOOT}')


def enable_ssh():
    print('Enabling SSH')
    mknod(BOOT + 'ssh')


def wifi_config():
    print('Configuring WiFi, user input required')    
    country = input('Country: ')
    ssid = input('SSID: ')
    psk = getpass('Password ', stream=None)
    
    wpa_supplicant = (
    f'country={country}\n'
    f'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n'
    f'update_config=1\n\n'
    f'network=\u007b\n' # {
    f'    ssid="{ssid}"\n'
    f'    psk="{psk}"\n'
    f'\u007d\n' # }
    )
    
    return wpa_supplicant


def enable_wifi():
    print('Enabling WiFi')
    
    with open(BOOT + 'wpa_supplicant.conf', 'w') as wifi_conf:
        wifi_conf.write(wifi_config())


def cleanup():
    print('Cleaning up')
    print('Unmounting SD')
    system(f'sudo umount {SD}*')
    print(f'Removing {TMP}')
    rmtree(TMP, ignore_errors=True)


if __name__ == '__main__':
    main()