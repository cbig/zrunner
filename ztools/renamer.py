#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import glob
import os
import sys

class ZRenamer(object):
    """ ZRenamer class for renaming Zonation variants.

    The functionality of this class' instances is restricted to replacing  variant name Strings in various places.
    """

    def __init__(self, variant_name, dir = '.'):
        """ Instantiate the class based on the original variant name.

        It is assumed that the variant has the following mandatory components:
            - bat-file
            - spp-file
            - dat-file

        Missing any of the option will cause an exception. Optionally, variant can have the following components:
            - variant subdir
            - result subdir

        The directories above may have arbitrarily complex path specification.

        @param variant_name String original name of the variant.
        @param dir String path to the directory to be searched (default: '.').
        """

        # Inititate instance attributes
        self.variant_name = variant_name

        # Try locating the needed file
        self.bat_file = glob.glob(os.path.join(dir, '*{0}*.bat'.format(variant_name)))
        if len(self.bat_file) == 0:
            print('ERROR: No bat-file found for variant {0} in directory {1}'.format(variant_name,
                                                                                     os.path.abspath(dir)))
            sys.exit(-1)


def main():
    parser = argparse.ArgumentParser(description='Rename Zonation variants')

    parser.add_argument('source_name', metavar='SRC_NAME', type=str,
                        help='Current variant name to be renamed')
    parser.add_argument('destination_name', metavar='DST_NAME', type=str,
                        help='New name')

    args = parser.parse_args()

    renamer = ZRenamer(args.source_name,)
    renamer.rename(args.destination_name)
