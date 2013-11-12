#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import platform
from subprocess import Popen, PIPE


class ZonationException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


def check_output_name(filename):
    ''' Checks for the existance of a given filename and creates a new and unused one if file
    already exists.

    @param filename String filename (abspath)
    @retun filenmae String possibly altered filename (basename)
    '''

    suffix = 1

    while os.path.exists(filename):
        base = os.path.basename(filename)
        base = base.split('.')
        if base[0].endswith('_{0}'.format(suffix - 1)):
            new_base = base[0].replace('_{0}'.format(suffix - 1), '_{0}'.format(suffix)) + '.' + base[1]
        else:
            new_base = base[0] + '_{0}'.format(suffix) + '.' + base[1]
        filename = os.path.join(os.path.dirname(filename), new_base)
        suffix += 1

    return filename


def get_system_info():
    ''' Function to retrieve system related information.

    @return list of system variables
    '''
    sys_info = []
    sys_info.append({'Report time': datetime.datetime.now().isoformat()})
    sys_info.append({'Uname': platform.uname()})

    if platform.system() == 'Linux':
        sys_info.append({'Version': platform.linux_distribution()})
    else:
        sys_info.append({'Version': platform.win32_ver()})

    return sys_info


def get_zonation_info():
    ''' Function to retrieve Zonation version info.

    NOTE: Zonation must be in PATH.

    @return tuple Zonation version number
    '''
    version = Popen(['zig3', '-v'], stdout=PIPE)
    version = version.communicate()[0]
    version = version.split('\n')[0].strip()
    version = version.split(':')[1].strip()
    version = tuple(version.split('.'))

    return version


def pad_header(msg, print_width):

    # - 4 is for 2 leading stars and 2 whitespaces
    nstars = print_width - len(msg) - 4
    return '\n** ' + msg + ' ' + '*' * nstars
