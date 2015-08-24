#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import glob
import os
import platform
from subprocess import Popen, PIPE
import sys

class ZonationRuninfoException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


def check_output_name(filename):
    """ Checks for the existence of a given filename and creates a new and
    unused one if file already exists.

    :param filename: String filename (abspath)

    :return filename: String possibly altered filename (basename)
    """

    suffix = 1

    while os.path.exists(filename):
        base = os.path.basename(filename)
        base = base.split('.')
        prev_id = '_{0}'.format(suffix - 1)
        cur_id = '_{0}'.format(suffix - 1)
        if base[0].endswith(prev_id):
            new_base = base[0].replace(prev_id, cur_id) + '.' + base[1]
        else:
            new_base = base[0] + '_{0}'.format(suffix) + '.' + base[1]
        filename = os.path.join(os.path.dirname(filename), new_base)
        suffix += 1

    return filename


def display_time(seconds, granularity=2):
    """ Get input time in seconds and convert into more convenient time formats.

    :param seconds: int number of seconds to be converted.
    :param granularity: int (>1) controlling the components returned. E.g.
      >>> display_time(133300)
      '1 day, 13 hours'
      >>> display_time(133300, granularity=4)
      '1 day, 13 hours, 1 minute, 40 seconds'

    :return String representation of the time provided.
    """

    intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


def find_file(filename, search_dir):
    """Search for a file in a directory.

    :param filename: String filename to be searched.
    :param search_dir: String path to the directory to be searched.
    :return: String path to match, else None.
    """

    # NOTE: Matching here allows for characters before but not after the match
    target_file = glob.glob(os.path.join(search_dir, filename))
    if len(target_file) == 0:
        print('ERROR: File {0} not found in directory {1}'.format(filename, os.path.abspath(search_dir)))
        sys.exit(-1)
    elif len(target_file) > 1:
        print('WARNING: More than one matching bat file found, using the first match {0}'.format(target_file[0]))

    target_file = target_file[0]

    return target_file


def get_system_info():
    """ Function to retrieve system related information.

    :return list of system variables
    """
    sys_info = []
    sys_info.append({'Report time': datetime.datetime.now().isoformat()})
    sys_info.append({'Uname': platform.uname()})

    if platform.system() == 'Linux':
        sys_info.append({'Version': platform.linux_distribution()})
    else:
        sys_info.append({'Version': platform.win32_ver()})

    return sys_info


def get_zonation_info(executable='zig4'):
    """ Function to retrieve Zonation version info.

    NOTE: Zonation must be in PATH.

    :param executable: String name of the Zonation executable (default: 'zig4').

    :return tuple Zonation version number
    """
    version = Popen([executable, '-v'], stdout=PIPE)
    version = version.communicate()[0]
    version = version.split('\n')[0].strip()
    version = version.split(':')[1].strip()
    version = tuple(version.split('.'))

    return version


def pad_header(msg, print_width, char='*'):
    """ Pad a given message with given character.

    :param msg: String message to be padded with '*'
    :param print_width: int number defining the print width
    :param char: Character used for padding (default: '*').
    :return: String padded message.
    """

    # - 4 is for 2 leading stars and 2 whitespaces
    nstars = print_width - len(msg) - 4
    return '\n{0}{1} '.format(char, char) + msg + ' ' + char * nstars


def parse_bat(bat_file):
    """ Parse Zonation bat-file.

    :param bat_file: String path to the bat-file to be parsed.
    :return: dict containing the parsed values.
    """

    cmd_components = {}

    with open(bat_file, 'r') as f:
        read_data = f.readlines()

        # NOTE: for now it assumed that each bat-file only has 1 line.
        if len(read_data) > 1:
            print('WARNING: bat-file {0} has more than 1 line, using only the first line'.format(bat_file))
        read_data = read_data[0]
        read_data = read_data.replace('\r', '')
        read_data = read_data.replace('\n', '')
        read_data = read_data.split(' ')

        # Assume a length of 10
        if len(read_data) != 10:
            print('WARNING: number of command components in bat-file {0} != 10, results may be wrong'.format(bat_file))

        try:
            # Get the individual command components
            cmd_components['command'] = read_data[0]
            cmd_components['executable'] = read_data[1]
            cmd_components['run_type'] = read_data[2]
            cmd_components['dat_file'] = read_data[3]
            cmd_components['spp_file'] = read_data[4]
            cmd_components['output'] = read_data[5]
            cmd_components['uncert_alpha'] = read_data[6]
            cmd_components['ds'] = read_data[7]
            cmd_components['aplha_multip'] = read_data[8]
            cmd_components['close_window'] = read_data[9]
        except IndexError, e:
            print('ERROR: bat-file has unusual content')

    return cmd_components