#!/usr/bin/env python

import sys, os, re, math
import numpy as np
import subprocess as subproc
import imp
#sys.path.append('../lib/RMSD/')
#import calculate_rmsd as rmsd
rmsd = imp.load_source("RMSD", "../lib/RMSD/calculate_rmsd")

def get_RMS_deviation(mol1, mol2):
    """
    Return the root-mean-square deviation between 2 geometries given in XYZ format.
    https://github.com/charnley/rmsd
    """
    RMSdev = {}
    atomsP, P = rmsd.get_coordinates(mol1)
    atomsQ, Q = rmsd.get_coordinates(mol2)

    # Calculate 'dumb' RMSD
    normal_rmsd = rmsd.rmsd(P, Q)

    # Create the centroid of P and Q which is the geometric center of a
    # N-dimensional region and translate P and Q onto that center.
    # http://en.wikipedia.org/wiki/Centroid
    Pc = rmsd.centroid(P)
    Qc = rmsd.centroid(Q)
    P -= Pc
    Q -= Qc
    RMSdev["Normal RMSD"] = normal_rmsd
    RMSdev["Kabsch RMSD"] = rmsd.kabsch_rmsd(P, Q)
    RMSdev["Fitted RMSD"] = rmsd.fit(P, Q)
    return RMSdev
    

# ============================================================================ #
# Testing
# ============================================================================ #
if __name__ == "__main__":
    path_to_file1 = "./files/Histidine_input.xyz"
    path_to_file2 = "./files/Histidine_optimized.xyz"
    RMSdev = get_RMS_deviation(path_to_file1, path_to_file2)
    print RMSdev
    RMSdev = get_RMS_deviation(path_to_file1, path_to_file1)
    print RMSdev
