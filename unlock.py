#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SkyEmie_' 💜 https://github.com/SkyEmie
https://en.wikipedia.org/wiki/Luhn_algorithm
"""

import time
import os
import math

import configparser
from os import path

##########################################################################################################################

def tryUnlockBootloader():

    unlock      = False

    increment = int(luhn_checksum(imei)+math.sqrt(imei)*1024)
    algoOEMcode = int(progress.get(str(imei), 'last_attempt', fallback=1000000000000000)) #base
    if not str(imei) in progress:
        progress[str(imei)] = {}
    progress[str(imei)]['last_attempt'] = str(algoOEMcode)
    # Load possible previous progress
    progress.read(progress_file)

    while((unlock == False) and (algoOEMcode < 10000000000000000)):
        sdrout = str(os.system('fastboot oem unlock '+str(algoOEMcode)))
        sdrout = sdrout.split(' ')
        for i in sdrout:
            if i == 'success':
                unlock = True
                return(algoOEMcode)
        algoOEMcode+=increment
        progress.set(str(imei), 'last_attempt', str(algoOEMcode))
        with open(progress_file, 'w') as f:
            progress.write(f)
    return(-1)

def luhn_checksum(imei):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(imei)
    oddDigits = digits[-1::-2]
    evenDigits = digits[-2::-2]
    checksum = 0
    checksum += sum(oddDigits)
    for i in evenDigits:
        checksum += sum(digits_of(i*2))
    return checksum % 10

##########################################################################################################################
progress_file = 'progress.ini'
progress = configparser.ConfigParser()
if not path.exists(progress_file):
    with open(progress_file, 'w') as f:
        progress.write(f)
progress.read(progress_file)

print('\n\n           Unlock Bootloader script - By SkyEmie_\'')
print('\n\n  (Please enable USB DEBBUG and OEM UNLOCK if the device isn\'t appear..)')
print('  /!\ All data will be erased /!\\\n')
input(' Press any key to detect device..\n')

os.system('adb devices')


if progress.sections():
    print('The following IMEIs were already saved')
    print(*progress.sections(), sep = ', ')

def start_bruteforce():
    input('Press any key to reboot your device..\n')
    os.system('adb reboot bootloader')
    input('Press any key when your device is ready.. (This may take time, depending on your cpu/serial port)\n')
    codeOEM = tryUnlockBootloader()
    if codeOEM > 0:
        os.system('fastboot getvar unlocked')
        os.system('fastboot reboot')
        print('\n\nDevice unlock ! OEM CODE : '+codeOEM)
        print('(Keep it safe)\n')
    else:
        print('Could not find the OEM CODE')

imei = int(input('Type IMEI digit :'))
start = 'no'
if luhn_checksum(imei) == 0:
    start = 'yes'
else:
    print('IMEI number seems invalid.')
    start = input('Would you like to try anyway? (type \'yes\' or \'no\')')

if start == 'yes':
    start_bruteforce()

input('Press any key to exit..\n')
exit()
