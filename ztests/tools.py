#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
from pprint import pprint
import sys

import gdal
from gdalconst import *
import numpy
from scipy.spatial.distance import jaccard
from scipy.stats import kendalltau
import yaml

from utilities import check_output_name


def raster_differences(raster_dataset_1, raster_dataset_2, tolerance=1e-08):
    ''' Compares the values of two rasters given a certain treshold.

    The default tolerance value is the same as the one used by numpy.allclose.

    @param raster_dataset_1 GDAL dataset
    @param raster_dataset_2 GDAL dataset
    @param tolerance double defining the raster similarity tolerance (see http://docs.scipy.org/doc/numpy/reference/generated/numpy.allclose.html)
    @return differences dict holding information on the potential differences
    '''

    differences = {}

    print("INFO: Extracting bands from the first dataset...")
    band_1 = raster_dataset_1.GetRasterBand(1)
    print("INFO: Extracting bands from the second dataset...")
    band_2 = raster_dataset_2.GetRasterBand(1)

    print("INFO: Extracting band 1 from the first dataset...")
    data_1 = band_1.ReadAsArray(0, 0, raster_dataset_1.RasterXSize,
                                raster_dataset_1.RasterYSize).astype(numpy.float)
    print("INFO: Extracting band 1 from the second dataset...")
    data_2 = band_2.ReadAsArray(0, 0, raster_dataset_2.RasterXSize,
                                raster_dataset_2.RasterYSize).astype(numpy.float)

    print("INFO: Comparing values...")
    equal = numpy.allclose(data_1, data_2, atol=tolerance)

    if not equal:
        print("WARNING: Raster dataset values not equal at {0} tolerance".format(tolerance))
        diff = data_1 - data_2

        differences['max'] = float(numpy.max(diff))
        differences['min'] = float(numpy.min(diff))
        differences['mean'] = float(numpy.mean(diff))
        differences['std'] = float(numpy.std(diff))
        #differences['quantiles'] = [float(item) for item in mquantiles(diff)]
        print("INFO: Calculating Kendall's tau statistics, this may take a while...")
        tau = kendalltau(data_1, data_2)
        differences['kendall_tau'] = (float(tau[0]), float(tau[1]))

        treshold = 0.99
        print("INFO: Calculating jaccard distance for treshold {0}".format(treshold))
        frac_data_1 = data_1 >= treshold
        frac_data_1 = numpy.reshape(frac_data_1, frac_data_1.size)
        frac_data_2 = data_2 >= treshold
        frac_data_2 = numpy.reshape(frac_data_2, frac_data_2.size)
        # Calculate jaccard index instead of distance
        differences['jaccard'] = (treshold, float(1-jaccard(frac_data_1, frac_data_2)))

    return differences


def raster_pairs(folder1, folder2, suffix='', ext=''):
    ''' Scan two Zonation output folders and search for raster files with the same name.

    Additional arguments can be provided to define a known filename suffix and/or extension.

    @param folder1 String path to first folder
    @param folder2 String path to second folder
    @return list of tuples (pairs of paths in the two folders)
    '''

    pairs = []
    pattern = '*' + suffix + ext

    rasters_1 = glob.glob(os.path.join(folder1, pattern))
    if len(rasters_1) == 0:
        print('ERROR: No suitable files (pattern: {0}) found in folder 1'.format(pattern))
        sys.exit(0)

    rasters_2 = glob.glob(os.path.join(folder2, pattern))
    if len(rasters_2) == 0:
        print('ERROR: No suitable files (pattern: {0}) found in folder 2'.format(pattern))
        sys.exit(0)

    raster_names_2 = [os.path.basename(item) for item in rasters_2]

    for raster_1 in rasters_1:

        raster_name_1 = os.path.basename(raster_1)

        # FIXME: rasters 2 indexing very fragile
        if raster_name_1 in raster_names_2:
            pairs.append((raster_1,
                          rasters_2[raster_names_2.index(raster_name_1)]))
        else:
            print('WARNING: Raster {0} not found in other folder'.format(raster_name_1))
            pprint(rasters_2)
            rasters_1.remove(raster_1)

    if not rasters_1:
        print('ERROR: none of the rasters in folder 1 found in folder 2')
        sys.exit(0)

    print(pairs)
    return pairs

if __name__ == '__main__':

    folder_1 = '/home/jlehtoma/opt/zonation-3.1.9-GNU-Linux/ztests/ESMK/output_linux_LH2-BIOTI25'
    folder_2 = '/home/jlehtoma/opt/zonation-3.1.9-GNU-Linux/ztests/ESMK/output_windows_LH2-BIOTI25'

    pairs = raster_pairs(folder_1, folder_2, suffix='.rank.*', ext='.img')

    all_differences = []

    for pair in pairs:

        if os.path.basename(pair[0]) != os.path.basename(pair[1]):
            print('WARNING: comparing raster datasets with different names')

        print("INFO: Reading in FIRST dataset {0}".format(pair[0]))
        raster_dataset1 = gdal.Open(pair[0], GA_ReadOnly)
        print("INFO: Reading in SECOND dataset {0}".format(pair[1]))
        raster_dataset2 = gdal.Open(pair[1], GA_ReadOnly)

        differences = raster_differences(raster_dataset1, raster_dataset2)
        if differences:
            differences['file1'] = pair[0]
            differences['file2'] = pair[1]

        all_differences.append(differences)

    for diff in all_differences:
        if diff:
            pprint(diff)
        else:
            print("INFO: All values in all pairs seem to be the same")

    output_file = check_output_name('raster_differences.yaml')
    with open(output_file, 'w') as outfile:
            outfile.write(yaml.dump(all_differences, canonical=True))
