#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from pprint import pprint
from subprocess import Popen
import sys
import time

from ztools.utilities import (check_output_name, display_time, get_system_info,
                              get_zonation_info, pad_header,
                              ZonationRuninfoException)

from ztools.parser import parse_results


def read_run(file_list, executable=None):
    """Reads in the Zonation bat/sh files and return a dict of command
    sequences.

    If an item in the list does not exist, it is removed from the file list.

    @param file_list String list of input file paths
    @param executable String for overriding executable
    @return cmd_sequences list of common sequences

    """

    cmd_sequences = {}

    for file_path in file_list:

        try:
            f = open(file_path, 'r')
        except IOError:
            print('WARNING: File {0} does not exist'.format(file_path))
            continue

        # Read the input files and parse the Zonation call sequence. A single
        # bat/sh file can have more than 1 row
        with f:
            content = f.readlines()
            for sequence in content:
                # On Unix systems hashbang can be included, do not include it
                if not sequence.startswith("#!"):
                    # Strip the trailing newline
                    sequence = sequence.replace('\n', '')
                    sequence = sequence.replace('\r', '')
                    # Replace the file path slashes
                    sequence = sequence.replace('\\', '/')
                    # Get rid of .exe, Windows can handle this as well
                    sequence = sequence.replace('.exe', '')
                    # Split the sequence
                    sequence = sequence.split(' ')
                    # Remove 'call' arg
                    if 'call' in sequence:
                        sequence.remove('call')
                    # Override executable if provided
                    if executable:
                        sequence[0] = executable

                    cmd_sequences[file_path] = sequence

    if cmd_sequences:
        return cmd_sequences
    else:
        print('ERROR: None of the input files exist')
        sys.exit(1)


def run_suite():
    pass


def run_analysis(file_path, cmd_args):
    """Zonation analysis runner.

    Runs a single analysis based on parsed arguments.

    @param file_path String path to the location where the bat
      file is located
    @param cmd_args list of Zonation command line arguments

    @return elapsed_times dict of seconds of analysis runtime
    """

    t0 = time.time()
    p = Popen(cmd_args, cwd=os.path.dirname(file_path))
    p.wait()

    t1 = time.time()

    total = t1 - t0

    # Get also the times reported by Zonation. Output name pattern is the 5th
    # item in the bat/sh file
    output_filepath = cmd_args[4]
    output_filepath = os.path.abspath(os.path.join(os.path.dirname(file_path),
                                                   output_filepath))
    try:
        elapsed_times = parse_results(output_filepath)
    except ZonationRuninfoException, e:
        print('ERROR: {0}'.format(e))
        elapsed_times = {'ERROR': str(e)}

    elapsed_times['measured'] = round(total, 0)

    return elapsed_times


def report_output(output_data, output_file=None, silent=False, print_width=80):

    if not silent:
        print(pad_header('SYSTEM INFO', print_width))
        pprint(output_data['sys_info'], width=print_width)
        print(pad_header('ZONATION INFO', print_width))
        print('Zonation version number: {0}'.format(output_data['z_info']))
        print(pad_header('BENCHMARK INFO', print_width))

        keys = output_data.keys()
        keys.sort()
        for key in keys:
            if key not in ['sys_info', 'z_info']:
                print('{0}:'.format(key))
                pprint(output_data[key], width=print_width)
    if not silent and output_file:
        import yaml
        with open(output_file, 'w') as outfile:
            outfile.write(yaml.dump(output_data, canonical=True))
        print('\nINFO: Wrote results in file {0}'.format(output_file))


def main():
    parser = argparse.ArgumentParser(description='Run Zonation runs and' +
                                                 'performance benchmarks.')

    parser.add_argument('input_files', metavar='INPUTS', type=str, nargs='?',
                        help='input bat/sh file')
    parser.add_argument('-l', '--load', dest='input_yaml', metavar="YAMLFILE",
                        help='yaml file defining a suite of input files')
    parser.add_argument('-x', '--executable', dest='executable',
                        default='zig4',
                        help='select Zonation executable (must in PATH)')
    parser.add_argument('-o', '--outputfile', dest='output_file', default='',
                        help='name of the output file')
    parser.add_argument('-w', '--overwrite', dest='overwrite', default=False,
                        help='overwrite existing result file')
    parser.add_argument('-s', '--silent', dest='silent', action='store_true',
                        help='run everything silent')
    parser.add_argument('--slack-config', dest='slack_config', default='',
                        help='Slack configuration file')

    args = parser.parse_args()

    slack_log = False

    if args.input_yaml:
        if args.input_files:
            print('WARNING: Both positional input files and loadable yaml ' +
                  'file defined. Using positional input files.')
        else:
            import yaml
            try:
                f = open(args.input_yaml, 'r')
            except IOError:
                print('ERROR: Input YAML file {0} does not ' +
                      'exist'.format(args.input_yaml))
                sys.exit(1)
            with f:
                suite = yaml.safe_load(f)
                args.input_files = suite['runs']
            # YAML file definitions can include relative paths that
            # need to be dealt with.
            relative_path = os.path.dirname(args.input_yaml)
            if relative_path:
                # Get the absolute path of the YAML file
                full_yaml_path = os.path.abspath(args.input_yaml)
                # Remove the relative YAML path from the absolute resulting
                # in a parent path
                parent_path = full_yaml_path.replace(args.input_yaml, '')
                abs_paths = []
                for input_file in args.input_files:
                    # Get just the file name of a give path within the YAML
                    # file
                    file_name = os.path.basename(input_file)
                    # Join the file name together with the parent path thus
                    # fixing the relative path
                    abs_path = os.path.join(parent_path,
                                            file_name)
                    abs_paths.append(abs_path)
                args.input_files = abs_paths

    elif not args.input_files:
        parser.print_help()
        sys.exit(2)

    # Single argument is not a list, loading a YAML file will produce a list.
    if not isinstance(args.input_files, list):
        args.input_files = [args.input_files]

    args.input_files = [os.path.join(os.path.abspath(__file__),
                        os.path.abspath(item)) for item in args.input_files]

    cmd_args = read_run(args.input_files, args.executable)

    # Notify to slack if configured
    if args.slack_config:
        import slackpy
        import yaml
        try:
            f = open(args.slack_config, 'r')
            with f:
                slack_config = yaml.safe_load(f)
                slack_log = True

                if 'WEBHOOK_URL' not in slack_config.keys():
                    print('ERROR: Slack configuration file does not have WEBHOOK_URL defined')
                    print('Slack notifications will not be enabled.')
                    slack_log = False
                elif 'CHANNEL' not in slack_config.keys():
                    print('ERROR: Slack configuration file does not have CHANNEL defined')
                    print('Slack notifications will not be enabled.')
                    slack_log = False
                else:
                    webhook_url = slack_config['WEBHOOK_URL']
                    channel = slack_config['CHANNEL']
                    user_name = 'zlogger'
                    # Create a new logger instance.
                    slack_logger = slackpy.SlackLogger(webhook_url, channel, user_name)
        except IOError:
            print('ERROR: Input Slack configuration YAML file {0} does not exist'.format(args.slack_config))
            print('Slack notifications will not be enabled.')

    # Collect output to a dict
    output = {'sys_info': get_system_info()}
    output['z_info'] = get_zonation_info(args.executable)

    if slack_log:
        z_version = '-'.join(output['z_info'])
        sys_name = '{0} ({1})'.format(output['sys_info'][1]['Uname'][1], output['sys_info'][1]['Uname'][0])
        sys_time = output['sys_info'][0]['Report time']
        msg = 'Starting runs using Zonation version <{0}> on {1} at {2}'.format(z_version, sys_name, sys_time)
        slack_logger.info(title='Initializing runs', message=msg)

    # Run the actual analyses
    run_no = 1
    for file_path, _cmd_args in cmd_args.iteritems():
        if slack_log:
            run_name = os.path.basename(file_path).split('.')[0]
            slack_logger.info(title='Run {0} [{1}/{2}]'.format(run_name, run_no, len(cmd_args)), 
                              message='Starting run')

        output[file_path] = run_analysis(file_path, _cmd_args)
        
        if slack_log:
            slack_logger.info(title='Run {0} [{1}/{2}]'.format(run_name, run_no, len(cmd_args)), 
                              message='Run {0} finished in {1}'.format(run_name,
                                                                       display_time(output[file_path]['measured'])))

        run_no += 1

    if not args.silent:
        # Construct a suitable output name if it doesn't exist
        if args.output_file == '':
            uname0 = output['sys_info'][1]['Uname'][0]
            uname1 = output['sys_info'][1]['Uname'][1]
            args.output_file = ''.join(['results_', uname0.lower(), '_',
                                        uname1.replace('.', ''), '.yaml'])
            print('WARNING: No output file name provided,' +
                  ' using {0}'.format(args.output_file))
        if not args.overwrite and os.path.exists(args.output_file):
            extant = args.output_file
            args.output_file = check_output_name(args.output_file)
            print('WARNING: Output file {0} exists, using {1}'.format(extant,
                  args.output_file))

    report_output(output, args.output_file, args.silent)

    print('\nzrunner finished.\n')

if __name__ == '__main__':
    main()
