#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from ztests.utilities import ZonationRuninfoException


def parse_results(file_path):
    ''' Parses Zonation *.run_info.txt file to obtain time elapsed in different
    stages of the analysis.

    If a specified run info file cannot be found, raise an exception. If the
    file is found but is incomplete, raise an exception.

    @param file_path String path to a Zonation run info file
    @return elapsed_time dict holding the parsed time values
    '''

    elapsed_time = {}

    try:
        f = open(file_path, 'r')
    except IOError:
        msg = 'Input run info file {0} does not exist'.format(file_path)
        raise ZonationRuninfoException(msg)

    # Data loading and initialization is reported with message:
    # "Loaded data and initialized in X seconds"
    init_pattern = re.compile('(?<=Loaded data and initialized in )' +
                              '(.*)(?= seconds)')

    # Cell removal is reported with message:
    # "Done in X seconds"
    cellrem_pattern = re.compile('(?<=Done in )(.*)(?= seconds)')

    # Overall elapsed time is reported with message:
    # "Elapsed time : X ms"
    elapsed_pattern = re.compile('(?<=Elapsed time : )(.*)(?= ms)')

    # Zonation does not return any error codes and it creates
    # a runinfo file even if it does not finish. If a particular finishing
    # message is not found, assume that the process did not finish.
    finished_pattern = re.compile('(?<=ZIG3: DONE!)')

    with f:
        # Track whehter Zonation apparently finished
        finished = False
        for line in f.readlines():
            # NOTE: the following assumes a fixed order of appearance in the
            # text file
            if 'init' not in elapsed_time.keys():
                if init_pattern.findall(line):
                    value = init_pattern.findall(line)[0]
                    elapsed_time['init'] = int(value)
            elif 'cellrem' not in elapsed_time.keys():
                if cellrem_pattern.findall(line):
                    value = cellrem_pattern.findall(line)[0]
                    elapsed_time['cellrem'] = int(value)
            elif 'elapsed' not in elapsed_time.keys():
                if elapsed_pattern.findall(line):
                    # Reported time is milliseconds so it needs to be divided
                    # by 1000
                    value = elapsed_pattern.findall(line)[0]
                    elapsed_time['elapsed'] = int(value) / 1000
            elif 'finished' not in elapsed_time.keys():
                if finished_pattern.findall(line):
                    finished = True
                    # This is the final item
                    break

        if not finished:
            msg = 'Run info file {0} found but incomplete'.format(file_path)
            raise ZonationRuninfoException(msg)

    return elapsed_time
