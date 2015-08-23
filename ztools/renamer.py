#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import yaml


class ZRenamer(object):
    ''' ZRenamer class for renaming Zonation variants.

    Each instance of ZReader class corresponds to a single result
    (YAML) file.
    '''

    def __init__(self, input_file):
        # Inititate instance attributes
        self.results = {}
        self.time = None
        self.uname = None
        self.version = None
        self.zversion = None

        self.input_file = input_file
        self.parse_results(input_file)

    def print_cli(self, line_length=79):

        print('\n')
        header = 'SYSTEM INFO'
        header = '** ' + header + ' ' + '*' * (79 - 4 - len(header))
        print(header)
        print(self._pad_string('Test run time', self.time))
        print(self._pad_string('Test computer', self.uname['name']))
        print(self._pad_string('OS', self.uname['os']))
        print(self._pad_string('Kernel', self.uname['os_kernel']))
        print(self._pad_string('Architecture', self.uname['arch']))
        print('\n')
        print(self._pad_string('Zonation version', self.zversion))
        print('\n')

        header = 'RUNS'
        header = '** ' + header + ' ' + '*' * (79 - 4 - len(header))
        print(header)

        if self.results:
            run_names = self.results.keys()
            run_names.sort()
            for run_name in run_names:
                print('[' + run_name + ']')
                run_info = self.results[run_name]
                if 'ERROR' in run_info.keys():
                    print('The run was not executed succesfully:')
                    print(run_info['ERROR'])
                else:
                    print(self._pad_string('Time to initialize (Zonation)',
                                           run_info['init'],
                                           title_lenght=30) + ' s')
                    print(self._pad_string('Cell removal time (Zonation)',
                                           run_info['init'],
                                           title_lenght=30) + ' s')
                    print(self._pad_string('Total elapsed time (Zonation)',
                                           run_info['measured'],
                                           title_lenght=30) + ' s')

                print(self._pad_string('Total measured time (ztools)',
                                       run_info['measured'],
                                       title_lenght=30) + ' s')
                print('\n')
        else:
            print('WARNING: No results parsed by the reader.')

    def parse_results(self, input_file):
        ''' Read in the provided YAML file and parse results.

        Common result inforamation are parsed to object attributes.

        @param input_file String file path to the results YAML file.
        '''

        results = self._read_results(input_file)

        # First, get the system information
        try:
            sys_info_list = results.pop('sys_info')

            sys_info = {}
            # Convert a list of dicts into a single dict
            for item in sys_info_list:
                for key, value in item.iteritems():
                    sys_info[key] = value

            self.time = sys_info['Report time']
            uname = sys_info['Uname']
            self.uname = {'os': uname[0],
                          'name': uname[1],
                          'os_kernel': uname[2],
                          'arch': uname[4]}
            self.version = ' '.join(sys_info['Version'])

            self.zversion = '.'.join(results.pop('z_info'))

            # Remaining key-value pairs are the actual runs
            for run_file, run_info in results.iteritems():
                self.results[os.path.basename(run_file)] = run_info

        except KeyError, e:
            sys.stderr.write('ERROR: Missing key {0}\n'.format(e))

    def _pad_string(self, title, value, title_lenght=15, line_length=79):
        ''' Helper method to create consistent command line output.

        @param title String title label
        @param value String value label
        @param title_lenght int length of the title label
        @param line_length int lenght of the whole line
        @return title_value String
        '''
        # How much whitespace padding is needed
        n_pad_ws = title_lenght - len(title)
        value = str(value)
        title_value = ' ' * n_pad_ws + title + ': ' + value
        return title_value

    def _read_results(self, input_file):
        ''' Read in the provided YAML file of Zonation results.

        @param input_file String file path to the results YAML file.

        '''
        try:
            f = open(input_file, 'r')
        except IOError:
            sys.stderr.write('ERROR: Input YAML file {0}'.format(input_file) +
                             ' does not exist\n')
            sys.exit(1)
        with f:
            results = yaml.load(f)
        return results


def main():
    parser = argparse.ArgumentParser(description='Read ztests result file')

    parser.add_argument('input_file', metavar='INPUT', type=str,
                        help='input yaml file')

    args = parser.parse_args()

    reader = ZReader(args.input_file)
    reader.print_cli()
