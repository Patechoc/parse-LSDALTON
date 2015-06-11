#!/usr/bin/env python

import sys, os, re, math
import numpy as np
import read_LSDALTON_output as readLS
import subprocess as subproc

#with open('input.txt') ad f:
    #data = [map(int, row) for row in csv.reader(f)]

def get_compareInfoGradients(path_to_file1, path_to_file2=""):
    """return the difference between 2 gradients in matrix form,
    and its max/min absolute elements and RMS norm.
    Keyword arguments:
    diffGrad -- the matrix difference as a list of x,y,z components for each atom (symbol)
    """
    obj1 = readLS.get_infoGradient(path_to_file1)
    if (obj1==None):
        return None
    grad1 = obj1['gradient']
    nbAtom = len(grad1)
    if path_to_file2 != "":
        obj2 = readLS.get_infoGradient(path_to_file2)
        if (obj2==None):
            return None
        grad2 = obj2['gradient']
        assert (len(grad1) == len(grad2)), \
            "Comparing gradients of different size: %r atoms vs %r atoms" % (len(grad1), len(grad2) )
        diffMat = np.concatenate( [[grad1[atom][1]-grad2[atom][1]] for atom in range(0,len(grad1))])
    else:
        diffMat = np.concatenate( [[grad1[atom][1]] for atom in range(0,len(grad1))])
    absDiffMat = np.absolute(diffMat)
    diffObj = {}
    diffObj['matDiffGrad'] = diffMat
    diffObj['maxDiffGrad'] = np.amax(absDiffMat)
    diffObj['minDiffGrad'] = np.amin(absDiffMat)
    diffObj['meanDiffGrad'] = np.mean(diffMat)
    diffObj['varianceDiffGrad'] = sum( [(x-diffObj['meanDiffGrad'])**2 for x in diffMat.flatten()] )/(3.*nbAtom)
    diffObj['stdDevDiffGrad'] = math.sqrt(diffObj['varianceDiffGrad'])
    diffObj['rmsDiffGrad'] = math.sqrt(sum( [x*x for x in absDiffMat.flatten()])/(3.*nbAtom))
    return diffObj

# ============================================================================ #
# Testing
# ============================================================================ #
if __name__ == "__main__":
    path_to_file1 = "./files/lsdalton_files/lsdalton20140924_geomOpt-b3lyp_Vanlenthe_6-31G_df-def2_Histidine_2CPU_16OMP_2014_10_28T1007.out"
    path_to_file2 = "./files/lsdalton_files/lsdalton20140924_b3lyp_gradient_ADMM2_6-31Gs_df-def2_3-21G_Histidine_8CPU_16OMP_2014_11_17T1502.out"
    diffGrad = get_compareInfoGradients(path_to_file1, path_to_file2)
    print "comparing:\n  %r\n  %r" % (path_to_file1,path_to_file2)
    print "gradient differences:\n  RMS norm: %e\n  Max Abs:  %e\n  Min Abs:  %e" % (diffGrad['rmsDiffGrad'],diffGrad['maxDiffGrad'],diffGrad['minDiffGrad'])
