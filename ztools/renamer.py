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

    def __init__(self, variant_name, dir = '.', verbose = False):
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
        @param verbose boolean setting verbose logging.
        """

        # Inititate instance attributes
        self.variant_name = variant_name

        # Try locating the needed file
        # NOTE: Matching here allows for characters before but not after the match
        self.bat_file = glob.glob(os.path.join(dir, '*{0}.bat'.format(variant_name)))
        if len(self.bat_file) == 0:
            print('ERROR: No bat-file found for variant {0} in directory {1}'.format(variant_name,
                                                                                     os.path.abspath(dir)))
            sys.exit(-1)
        elif len(self.bat_file) > 1:
            print('WARNING: More than one matching bat file found, using the first match {0}'.format(self.bat_file[0]))

        self.bat_file = self.bat_file[0]
        if verbose:
            print("INFO: Found bat-file {0}".format(self.bat_file))



def main():
    parser = argparse.ArgumentParser(description='Rename Zonation variants')

    parser.add_argument('source_name', metavar='SRC_NAME', type=str, help='Current variant name to be renamed')
    parser.add_argument('destination_name', metavar='DST_NAME', type=str, help='New name')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False,
                        help='Enable verbose logging')

    args = parser.parse_args()

    renamer = ZRenamer(args.source_name, verbose=args.verbose)
    #renamer.rename(args.destination_name)
