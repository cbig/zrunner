#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def parse_results(file_path):
    ''' Parses Zonation *.run_info.txt file to obtain time elapsed in different stages of the
    analysis.

    If a specified run info file cannot be found, an empty dict is returned instead.

    @param file_path String path to a Zonation run info file
    @return elapsed_time dict holding the parsed time values
    '''

    elapsed_time = {}

    try:
        f = open(file_path, 'r')
    except IOError:
        print('WARNING: Input run info file {0} does not exist'.format(file_path))
        return elapsed_time

    # Data loading and initialization is reported with message:
    # "Loaded data and initialized in X seconds"
    init_pattern = re.compile('(?<=Loaded data and initialized in )(.*)(?= seconds)')

    # Cell removal is reported with message:
    # "Done in X seconds"
    cellrem_pattern = re.compile('(?<=Done in )(.*)(?= seconds)')

    # Overall elapsed time is reported with message:
    # "Elapsed time : X ms"
    elapsed_pattern = re.compile('(?<=Elapsed time : )(.*)(?= ms)')

    with f:
        for line in f.readlines():
            # NOTE: the following assumes a fixed order of appearance in the text file
            if 'init' not in elapsed_time.keys():
                if init_pattern.findall(line):
                    elapsed_time['init'] = int(init_pattern.findall(line)[0])
            elif 'cellrem' not in elapsed_time.keys():
                if cellrem_pattern.findall(line):
                    elapsed_time['cellrem'] = int(cellrem_pattern.findall(line)[0])
            elif 'elapsed' not in elapsed_time.keys():
                if elapsed_pattern.findall(line):
                    # Reported time is milliseconds so it needs to be divided by 1000
                    elapsed_time['elapsed'] = int(elapsed_pattern.findall(line)[0]) / 1000
                    # This is the final item
                    break

    return elapsed_time

if __name__ == '__main__':
    test_file = '/home/jlehtoma/opt/zonation-3.1.9-GNU-Linux/ESMK/analyysi/output/result_18_60_5kp_abf_pe_w_cmat_cmete.run_info.txt'
    print(parse_results(test_file))
