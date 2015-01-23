#!/usr/bin/env python 

import sys, os, re, math
import numpy as np
#from glob import glob
import subprocess as subproc
#import parserGrammar
#import csv

# http://pandas.pydata.org/

#with open('input.txt') ad f:
    #data = [map(int, row) for row in csv.reader(f)]


def get_infoGradient(path_to_file=""):
    """return a matrix form of the gradient, its max/min absolute elements and RMS norm.
    Keyword arguments:
    grad -- the molecular gradient as a list of x,y,z components for each atom (symbol)
    """
    gradString = get_last_molecular_gradient(path_to_file)
    obj = get_infoGradient_from_gradString(gradString)
    return obj
    
def get_infoGradient_from_gradString(gradString=[]):
    """return a matrix form of the gradient, its max/min absolute elements and RMS norm.
    Keyword arguments:
    gradString -- the molecular gradient as a list of x,y,z components for each atom (symbol)
    """
    matGrad  = np.array([[float(line[key]) for key in ['x','y','z']] for line in gradString])
    gradient = [[ line['atom'], np.array([float(line[key]) for key in ['x','y','z']]) ] for line in gradString]
    absGrad = np.absolute(matGrad)
    nbAtom = len(absGrad)
    obj = {}
    obj['gradient'] = gradient
    obj['maxGrad'] = np.amax(absGrad)
    obj['minGrad'] = np.amin(absGrad)
    obj['rmsGrad'] = math.sqrt((sum( [x*x for x in absGrad.flatten()]))/(3.*nbAtom))
    return obj
    

def get_last_molecular_gradient(path_to_file=""):
	assert os.path.exists(path_to_file) == 1
	# try finding the last "Molcular gradient"
	out = ""
	try:
		cmd= 'sed -n "/Molecular gradient/,/RMS gradient/p" '+path_to_file
		out1 = subproc.check_output(cmd, shell=True)
		#print out
		out2=out1.rsplit('-----------------------', 1)[1]
		out3=out2.rsplit('RMS gradient norm', 1)[0]
		out = [line.strip() for line in out3.split('\n') if line.strip() != '']
	except:
		print "Not able to extract the molecular gradient from this file:\n", path_to_file
		
	## reBuild the gradient matrix
	# using FOR LOOP
	#grad = []
	#for i,line in enumerate(out):
		#[atom,x,y,z] = line.split()
		#obj = {}
		#obj["atom"] = atom
		#obj["x"] = x
		#obj["y"] = y
		#obj["z"] = z
		#grad.append(obj)
	#print grad
	#print atom,x,y,z
	
	# reBuild the gradient matrix
	# using dict comprehension syntax version
	grad = np.array([ {key: value for (key, value) in zip(["atom","x","y","z"], line.split())} for line in out])
	return grad


def get_MOL_string(filename):
    cmd= 'sed -n "/PRINTING THE MOLECULE.INP FILE/","/PRINTING THE LSDALTON.INP FILE/p" '+filename + "| awk 'NR>3' | head -n -2"
    print cmd
    outString = check_output(cmd, shell=True)
    return outString


def get_DAL_string(filename):
    cmd= 'sed -n "/PRINTING THE LSDALTON.INP FILE/,/END OF INPUT/p" '+filename + "| awk 'NR>3'"
    print cmd
    outString = check_output(cmd, shell=True)
    return outString

def parse_DAL_string(string):
    # find out if LinK or ADMM
    # if ADMM, which ADMM
    # is it B3LYP, BLYP, camB3LYP
    print string
    
def parse_MOL_string(string):
    # get comment (hopefully name of the molecule)
    # count number of atoms, give the molecular formula
    # get number of electrons: nb_atoms*Z
    cmd= 'grep -i "Atoms="" '+filename
    print cmd
    outString = check_output(cmd, shell=True)
    return outString


# ============================================================================ #
# Class: DAL_input
# ============================================================================ #
class DAL_input(object):
    def __init__(self, molecule, inputKeywords, nb_procs = 1, nb_threads = 1, revisionGIT = None):
#    def __init__(self, jobs, time, pause = 60):
        self.ismolecule = molecule
        self.inputKeywords = inputKeywords
        self.nb_proc = nb_proc
        self.nb_threads = nb_threads
        self.revisionGIT = revisionGIT


# ============================================================================ #
# Class: LSDALTONinput
# ============================================================================ #
class LSDALTONinput(object):
    def __init__(self, molecule, inputKeywords, nb_procs = 1, nb_threads = 1, revisionGIT = None):
#    def __init__(self, jobs, time, pause = 60):
        self.molecule = molecule
        self.inputKeywords = inputKeywords
        self.nb_proc = nb_proc
        self.nb_threads = nb_threads
        self.revisionGIT = revisionGIT


# ============================================================================ #
# Testing
# ============================================================================ #
if __name__ == "__main__":
    path_to_file = "./files/lsdalton_files/lsdalton20140924_geomOpt-b3lyp_Vanlenthe_6-31G_df-def2_Histidine_2CPU_16OMP_2014_10_28T1007.out"
    #path_to_file = "./files/lsdalton_files/lsdalton20140924_b3lyp_gradient_ADMM2_6-31Gs_df-def2_3-21G_Histidine_8CPU_16OMP_2014_11_17T1502.out"
	
    grad = get_last_molecular_gradient(path_to_file)
    gradInfo = get_infoGradient_from_gradString(grad)
    print "\nExtracting gradient from:\n  %r\n" % (path_to_file)
    print "gradient informations:\n  RMS norm: %e\n  Max Abs:  %e\n  Min Abs:  %e" % (gradInfo['rmsGrad'],gradInfo['maxGrad'],gradInfo['minGrad'])

