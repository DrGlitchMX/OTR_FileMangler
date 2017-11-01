# coding=utf-8
"""
Created on 2014-01-08

@author: defiler
"""


# Do not process files if they are opened by a process belonging to these users.
FILE_USERS = ['proftpd',]

# directory which is scanned for incoming movies and series
SOURCE_PATH = '/opt/ftp'
# base path of movie and series collection
TARGET_BASE_PATH = '/mnt/nasgul.castle/Videos'
# file for keeping track of already processed files
PROCESSED_FILES = '/opt/ftp/otr_processed_files'

MOVIES_SUBDIR = 'filme'
SERIES_SUBDIR = 'series'

# Currently used for series, only. Specify what subdirectories
# of SERIES_SUBDIR you want covered.
# If series naming occurrs in a unreliable way, specify alternative
# names as additional entries in the tuple. The first entry will always
# be regarded as the actual folder name.
CATEGORIES = {
    SERIES_SUBDIR : [
        ('American Dad',),
        ('Buffy',),
        ('CSI',),
        ('Family Guy',),
        ('Farscape',),
        ('Futurama',),
        ('House MD',),
        ('Law and Order', 'Law und Order', 'Law Order',),
        ('Navy CIS', 'NCIS',),
    ]
}

