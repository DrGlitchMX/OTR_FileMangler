# coding=utf-8
'''
Created on 08.01.2014

@author: defiler
'''


# Do not process files if they are opened by a process belonging to these users.
FILE_USERS = ['proftpd',]

# directory which is scanned for incoming data
SOURCE_PATH = '/share/Ftp'
# base path of movie and series collection
TARGET_BASE_PATH = '/share/Videos'
# file for keeping track of already processed files
PROCESSED_FILES = '/opt/ftp/otr_processed_files'


CATEGORIES = ['filme', 'series', 'doku', 'misc',]
SUB_CATEGORIES = {
        'filme' : None,
        'series' : [('American Dad',),
                    ('Angel',),
                    ('BigBangTheory',),
                    ('Bones',),
                    ('Buffy',),
                    ('Charmed',),
                    ('CSI',),
                    ('Criminal Intent',),
                    ('Dead Like Me',),
                    ('Der Tatortreiniger',),
                    ('Die Anstalt',),
                    ('Dr. House',),
                    ('Family Guy',),
                    ('Farscape',),
                    ('Firefly Season',),
                    ('Futurama',),
                    ('Grey s Anatomy',),
                    ('Harvey Birdman',),
                    ('heroes',),
                    ('Homeland',),
                    ('House MD',),
                    ('IjonTichy',),
                    ('Irgendwie und Sowieso',),
                    ('Law and Order', 'Law und Order', 'Law Order',),
                    ('Lilyhammer',),
                    ('Mord mit Aussicht',),
                    ('Navy CIS', 'NCIS',),
                    ('Orphan Black',),
                    ('Revenge',),
                    ('Robot Chicken',),
                    ('Sex and the City',),
                    ('The Mentalist',),],
        'doku' : None,
        'misc' : None,
        }


