# coding=utf-8
#!/usr/bin/env python
'''
Fetch files in FTP incoming directory, rename them properly
and move them to appropriate positions for easier pickup by
DLNA servers, e.g.

Created on 08.01.2014

@author: defiler
'''


import os
import re
import time
from settings import *

def find_files(start_dir):
    """
    Obtain files from the given directory.
    Only files with a specified @minimum_age are included
    in order to avoid interference with files currently being downloaded.
    """

    minimum_age = 60 * 3 # seconds
    target_files = set()

    for r, d, files in os.walk(start_dir):
        del r, d # our FTP incoming dir has no sub-hierarchy
        files.sort()
        for fn in files:
            try:
                vid_file_path = os.path.join(start_dir, fn)
                vid_file = open(vid_file_path)
                if vid_file:
                    print time.ctime(), "Trying file ", vid_file_path
                    mtime = os.fstat(vid_file.fileno()).st_mtime
                    file_modify_age_s = time.time() - mtime
                    vid_file.close()
                    if file_modify_age_s > minimum_age:
                        target_files.add(fn)
                        print time.ctime(), "Moving file, age is okay (", file_modify_age_s, "s)"
                    else:
                        print time.ctime(), "Not moving file, too young(", file_modify_age_s, "s)"
            except Exception as e:
                pass

    return target_files

def adapt_name(orig, keep_date=False):
    """
    Perform basic filtering on the crude file names assigned by OTR.
    Station name etc are stripped, date and time are retained.
    """
    pattern = re.compile(r'^(?:[0-9]+_)?(?P<title>[\w-]+)_'
        + r'(?P<season_episode>S\|s][0-9]+E\|s[0-9]+_)?'
        + r'(?P<date>[0-9]{2}\.[0-9]{2}\.[0-9]{2})_'
        + r'(?P<time>[0-9]{2}-[0-9]{2})'
        + r'.*(?P<extension>\.avi|\.mp4|\.mpg)')

    match = pattern.match(orig)
    if match:
        nice_title = match.group('title').replace('_', ' ')
        season_episode = match.group('season_episode')
        if season_episode:
            season_episode = ' ' + season_episode.replace('_', ' ')
        else:
            season_episode = ''
        date = match.group('date').replace('.', '-')
        time = match.group('time')
        extension = match.group('extension')
        if keep_date:
            nice_title += '{0} 20{1}_{2}{3}'.format(season_episode, date, time, extension)
        else:
            nice_title += extension
        return nice_title
    else:
        print "No match for", orig
    return orig


def move_file(orig_path, new_path):
    fOrig = open(orig_path, 'r')
    if fOrig is None:
        print time.ctime(), "Cannot move original file!"
        return
    fOrig.close()


    def next_filename_num(base_path, num=None):
        if num is None:
            num = 0
            try:
                f = open(base_path, 'r')
            except Exception as e:
                return base_path
            if f:
                f.close()
                return next_filename_num(base_path, num)
        else:
            try:
                f = open(base_path, 'r')
            except Exception as e:
                return base_path
            if f:
                f.close()
                pStr = r'(?P<extension>\.\w{3,4})(\.(?P<dup_num>\d+))?$'
                pat = re.compile(r'.*' + pStr)
                match = pat.match(base_path)
                if match:
                    extension = match.group('extension')
                    dup_num = int(match.group('dup_num') or num)
                    dup_num += 1
                    base_path = re.sub(pStr,
                                      extension + '.' + str(dup_num),
                                      base_path)
                    return next_filename_num(base_path, dup_num)
                else:
                    return next_filename_num(base_path)

    new_path = next_filename_num(new_path)

    print time.ctime(), "Moving: '{0}'\n    to '{1}'".format(orig_path, new_path)
    os.rename(orig_path, new_path)

def arrange_series(dict_series_names):
    total_num_series = len([i for i in dict_series_names.values() if len(i) > 0])
    if total_num_series > 0:
        print time.ctime(), '\n########'
        print time.ctime(), "Arranging series:"
    for series, episodes in dict_series_names.items():
        for e in episodes:
            try:
                orig_path = os.path.join(SOURCE_PATH, e)
                
                new_path = os.path.join(TARGET_BASE_PATH, 'series',
                                        series, adapt_name(e, True))
                move_file(orig_path, new_path)
            except Exception as ex:
                print time.ctime(), ex
            finally:
                print time.ctime(), series, "\n\t", e

    if total_num_series > 0:
        print time.ctime(), '\n########'

def arrange_movies(raw_names):
    if len(raw_names) > 0:
        print time.ctime(), '\n########'
        print time.ctime(), "Arranging movies:"
    for m in raw_names:
        try:
            orig_path = os.path.join(SOURCE_PATH, m)
            new_path = os.path.join(TARGET_BASE_PATH, 'filme', adapt_name(m, False))
            move_file(orig_path, new_path)
        except Exception as e:
            print time.ctime(), e
        finally:
            print time.ctime(), 'filme:', m

    if len(raw_names) > 0:
        print time.ctime(), '\n########'

def find_series(orig_names):
    """
    Check for files matching a series that already has a proper
    sub-directory.
    If so, they are added to a dictionary of "series" : [ list of files ]
    for further processing
    """
    series = SUB_CATEGORIES['series']

    series_episodes = {s[0] : [] for s in series}

    for orig in orig_names:
        for ser in series:
            for name in ser:
                if name.lower() in orig.lower():
                    series_episodes[ser[0]].append(orig)
                elif name.lower() in re.sub('_', ' ', orig.lower()):
                    series_episodes[ser[0]].append(orig)
    return series_episodes


def re_arrange_files(start_dir):
    """
    Comprehensive collection and re-arrangement function.
    """
    orig_file_names = find_files(start_dir)
    orig_series_names = find_series(orig_file_names)

    series_files = []
    for e in orig_series_names.values():
        if len(e) > 0:
            for f in e:
                series_files.append(f)

    orig_movies_names = []
    for f in orig_file_names:
        if not f in series_files:
            orig_movies_names.append(f)

    arrange_series(orig_series_names)
    arrange_movies(orig_movies_names)


if __name__ == '__main__':
    re_arrange_files(SOURCE_PATH)

