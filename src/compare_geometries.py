#!/usr/bin/env python

import sys, os, re, math
import numpy as np
import subprocess as subproc


def get_RMS_deviation(path_to_file1, path_to_file2):
    """
    Return the root-mean-square deviation between 2 geometries given in XYZ format.
    https://github.com/charnley/rmsd
    """
    RMSdev = None

    return RMSdev
    

# ============================================================================ #
# Testing
# ============================================================================ #
if __name__ == "__main__":
    path_to_file1 = "./files/lsdalton_files/lsdalton20140924_geomOpt-b3lyp_Vanlenthe_6-31G_df-def2_Histidine_2CPU_16OMP_2014_10_28T1007.out"
    RMSdev = get_RMS_deviation(path_to_file1, path_to_file2)
