#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

from ztools.utilities import find_file


class ZRenamer(object):
    """ ZRenamer class for renaming Zonation variants.

    The functionality of this class' instances is restricted to replacing  variant name Strings in various places.
    """

    def __init__(self, variant_name, search_dir='.', verbose=False):
        """ Instantiate the class based on the original variant name.

        It is assumed that the variant has the following mandatory components:
            - bat-file
            - spp-file
            - dat-file

        Missing any of the option will cause an exception. Optionally, variant can have the following components:
            - variant subdir
            - result subdir

        The directories above may have arbitrarily complex path specification.

        :param variant_name: String original name of the variant.
        :param search_dir: String path to the directory to be searched (default: '.').
        :param verbose: boolean setting verbose logging.
        """

        # Initiate instance attributes
        self.variant_name = variant_name

        # Try locating the needed files
        self.bat_file = find_file('*{0}.bat'.format(variant_name), search_dir)
        if self.bat_file and verbose:
            print("INFO: Found bat-file {0}".format(self.bat_file))

        self.bat_file = find_file('*{0}.bat'.format(variant_name), search_dir)
        if self.bat_file and verbose:
            print("INFO: Found bat-file {0}".format(self.bat_file))



def main():
    parser = argparse.ArgumentParser(description='Rename Zonation variants')

    parser.add_argument('source_name', metavar='SRC_NAME', type=str, help='Current variant name to be renamed')
    parser.add_argument('destination_name', metavar='DST_NAME', type=str, help='New name')
    parser.add_argument('-d', '--dir', metavar='DIR', nargs='?', type=str, default=os.getcwd(),
                        help='Path to search directory')
    parser.add_argument('-k', '--keep', action='store_true', dest='keep', default=False,
                        help='Keep original')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False,
                        help='Enable verbose logging')

    args = parser.parse_args()

    renamer = ZRenamer(args.source_name, search_dir=args.dir, verbose=args.verbose)
    #renamer.rename(args.destination_name)
