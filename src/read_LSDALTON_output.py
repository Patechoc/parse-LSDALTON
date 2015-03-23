#!/usr/bin/env python 

import sys, os, re, math
import numpy as np
import subprocess as subproc
from parser import *
import molecule as mol
import Inputs_DALTON as dalton


# http://pandas.pydata.org/


# # ============================================================================ #
# # Class: MOL_input
# # ============================================================================ #
# class MOL_input(object):
#     def __init__(self):
#         self.inputString = ""
#         self.format      = "" # BASIS or ATOMBASIS
#         self.basis

# # ============================================================================ #
# # Class: MOL_output
# # ============================================================================ #
# class MOL_output(object):
#     def __init__(self):
#         self.outputString = ""
#         self.format      = "" # BASIS or ATOMBASIS
        

#     def get_coordinates_XYZ(self):
#         '''https://github.com/charnley/rmsd'''
#         return True

# # ============================================================================ #
# # Class: LSDALTON_calculation
# # ============================================================================ #
# class LSDALTON_calculation(object):
#     def __init__(self):
# #    def __init__(self, jobs, time, pause = 60):
#         self.MOL_input   = None
#         self.DAL_input   = None
#         self.nb_procs    = nb_procs
#         self.nb_threads  = nb_threads
#         self.revisionGIT = revisionGIT

def getShortFilename(path_to_file):
    return os.path.basename(path_to_file).split('.')[0]

def get_input_MOL_string(filename):
    cmd= 'sed -n "/PRINTING THE MOLECULE.INP FILE/","/PRINTING THE LSDALTON.INP FILE/p" ' + filename + "| awk 'NR>3' | head -n -2"
    outString = subproc.check_output(cmd, shell=True)
    ## strip each line from the extraced string
    output = "\n".join([line.strip() for line in outString.split('\n')])
    return output

def get_optmized_MOL_string(filename):
    cmd='sed -n "/Final geometry (au)/","/Optimization information/p" ' + filename + "| awk 'NR>3' | head -n -2"
    outString = subproc.check_output(cmd, shell=True)
    ## strip each line from the extraced string
    output = "\n".join([(line.strip()[2:]).strip() for line in outString.split('\n')])
    return output


def parse_molecule_input(path_to_file):
    molString = get_input_MOL_string(path_to_file)
    #print molString
    daltonFormat = molString.split("\n")[0].strip()
    if daltonFormat == "BASIS":
        inputDALTON = parse_input_MOL_string_BASIS(molString) ## get DALTON info about basis, mol. charge, ..
        inputDALTON.name = getShortFilename(path_to_file)
        inputDALTON.shortname = inputDALTON.name
        listAtoms  = parse_input_MOL_string_atomCoord(molString)  ## get coordinates of atoms
        [inputDALTON.addAtomInfo(atom) for atom in listAtoms]
        inputDALTON.listAtoms = listAtoms
    elif daltonFormat == "ATOMBASIS":
        sys.exit("parsing of the 'ATOMBASIS' format not supported yet")
    else:
        sys.exit("DALTON molecule format not recognized: neither 'BASIS' nor 'ATOMBASIS'")
    return inputDALTON


def parse_input_MOL_string_BASIS(moleculeString):
    #print moleculeString
    inputDALTON = dalton.moleculeInput()
    get_infos =  Literal("BASIS").setResultsName("DaltonFormat") + EOL \
                 + StrangeName.setResultsName("regBase") \
                 + Optional(Literal("Aux=") + StrangeName.setResultsName("auxBase"))\
                 + Optional(Literal("ADMM=") + StrangeName.setResultsName("ADMMBase"))\
                 + EOL +  all.setResultsName("comment1") +  all.setResultsName("comment2") \
                 + Literal("Atomtypes=").suppress() + integer.setResultsName("nbAtomsTypes") \
                 + Optional(Literal("Charge=").suppress() + StrangeName.setResultsName("charge")) \
                 + all.setResultsName("unitDistances_and_symmmetry")
    # --- EXTRACT THE DATA
    if len(get_infos.searchString(moleculeString)) == 0:
        sys.exit("ERROR: Not able to extract meaningful information from this molecule string:\n"+moleculeString)
    for tokens in get_infos.searchString(moleculeString):
        #print tokens.dump()
        if tokens.regBase:        inputDALTON.regBasis = tokens.regBase
        if tokens.auxBase:        inputDALTON.auxBasis = tokens.auxBase
        if tokens.ADMMBase:       inputDALTON.admmBasis = tokens.ADMMBase
        if tokens.comment1 or tokens.comment2:       inputDALTON.comments = (tokens.comment1).strip() + " // " + (tokens.comment2).strip()
        if tokens.charge:   inputDALTON.charge = float(tokens.charge)
        if tokens.unitDistances_and_symmmetry:
            findAnyWords  = re.compile(ur'(\w+)')
            bohr_angstrom = re.compile(ur'(?i)(bohr|angstrom)')
            test_str = unicode(tokens.unitDistances_and_symmmetry)
            regexMatches = re.findall(findAnyWords, test_str)
            found_symmetry = [word for word in regexMatches if 'symm' in word]
            found_unitDistance = [word for word in regexMatches if len(re.findall(bohr_angstrom, word))]
            if len(found_symmetry) != 0: inputDALTON.usingSymmetry = found_symmetry[0].lower()
            if len(found_unitDistance) != 0:
                inputDALTON.unitDistance = found_unitDistance[0].lower()
            else:
                inputDALTON.unitDistance = 'Bohr'
    return inputDALTON

def parse_input_MOL_string_atomCoord(moleculeString):
    atomTypeInfos  =  Literal("Charge=").suppress() + StrangeName.setResultsName("chargeAtom") + Literal("Atoms=").suppress() + integer.setResultsName("nbAtoms") + EOL
    coordinate = Combine((Optional(Literal("-"))+Optional(integer)+Literal(".")+integer))
    AtomCoordinates = element.setResultsName("atomAbrev") + coordinate.setResultsName("xCoord") + coordinate.setResultsName("yCoord") + coordinate.setResultsName("zCoord") + EOL
    sameAtomCoordinates =  OneOrMore(AtomCoordinates.setResultsName("sameAtomCoord")).setResultsName("OneMoresameAtomCoord") 
    allAtoms = atomTypeInfos + sameAtomCoordinates
    matches = atomTypeInfos | AtomCoordinates
    listAtoms = []
    nbSameAtoms = -1
    chargeAtom = None
    for tokens in matches.searchString(moleculeString):
        #print tokens.dump()
        if tokens.chargeAtom != "": # new group
            chargeAtom = float(tokens.chargeAtom)
            nbSameAtoms = int(tokens.nbAtoms)
        else:
            atom = mol.atomInfos(atomSymbol=str(tokens.atomAbrev), atomCharge=chargeAtom)
            atom.xCoord = float(tokens.xCoord)
            atom.yCoord = float(tokens.yCoord)
            atom.zCoord = float(tokens.zCoord)
            listAtoms.append(atom)
    #print listAtoms
    return listAtoms

def parse_optimized_MOL_string_atomCoord(moleculeString):
    outputGeometryDALTON = dalton.moleculeInput()
    listAtoms = []
    # remove first 3 lines
    molStr = "\n".join(moleculeString.split("\n")[3:])
    coordinate = Combine((Optional(Literal("-"))+Optional(integer)+Literal(".")+integer))
    xcoord = Literal("x").suppress() + StrangeName
    ycoord = Literal("y").suppress() + StrangeName
    zcoord = Literal("z").suppress() + StrangeName
    AtomCoordinates = (element.setResultsName("atomAbrev") + xcoord.setResultsName("xcoord") + EOL + ycoord.setResultsName("ycoord") + EOL+ zcoord.setResultsName("zcoord") + EOL)
    matches = AtomCoordinates.searchString(moleculeString)
    for tokens in matches:
        atom = mol.atomInfos(atomSymbol=str(tokens.atomAbrev))
        atom.xCoord = float(tokens.xcoord[0])
        atom.yCoord = float(tokens.ycoord[0])
        atom.zCoord = float(tokens.zcoord[0])
        atom.unitDistance = 'Bohr'
        listAtoms.append(atom)
    [outputGeometryDALTON.addAtomInfo(atom) for atom in listAtoms]
    return outputGeometryDALTON


def parse_molecule_optimized(path_to_file):
    moleculeInputString = get_input_MOL_string(path_to_file)
    daltonFormat = moleculeInputString.split("\n")[0].strip()
    if daltonFormat == "BASIS":
        outputGeometryDALTON = parse_input_MOL_string_BASIS(moleculeInputString) ## get DALTON info about basis, mol. charge, ..
        outputGeometryDALTON.name = getShortFilename(path_to_file)
        outputGeometryDALTON.shortname = outputGeometryDALTON.name
    moleculeOptimizedString = get_optmized_MOL_string(path_to_file)
    #print moleculeOptimizedString
    if moleculeOptimizedString.strip() != "":
        optimizedGeometry = parse_optimized_MOL_string_atomCoord(moleculeOptimizedString)
        [outputGeometryDALTON.addAtomInfo(atom) for atom in optimizedGeometry.listAtoms]
    else:
        return None
    return outputGeometryDALTON


# def get_DAL_string(filename):
#     cmd= 'sed -n "/PRINTING THE LSDALTON.INP FILE/,/END OF INPUT/p" '+filename + "| awk 'NR>3'"
#     print cmd
#     outString = subproc.check_output(cmd, shell=True)
#     return outString

# def parse_DAL_string(string):
#     dal_input = {}
#     # find out if LinK or ADMM
#     # if ADMM, which ADMM
#     # is it B3LYP, BLYP, camB3LYP
#     return dal_input


def get_energy_contribution_nuclearRepulsion(path_to_file):
    """ returns an array
    of several nuclear repulsion contribution, one for each new
    geometry in the case of a geometry optimization,
    or of only one element for a single energy calculation"""
    cmd= "grep 'Nuclear repulsion:' "+ path_to_file.strip() + " | awk '{print $3}' "
    #print cmd
    out = subproc.check_output(cmd, shell=True)
    return out.strip().split('\n')
    
def get_energy_contribution_firstNuclearRepulsion(path_to_file):
    return float(get_energy_contribution_nuclearRepulsion(path_to_file)[0])

def get_energy_contribution_lastNuclearRepulsion(path_to_file):
    return float(get_energy_contribution_nuclearRepulsion(path_to_file)[-1])
    
def get_infoGradient(path_to_file):
    """return a matrix form of the gradient, its max/min absolute elements and RMS norm.
    Keyword arguments:
    grad -- the molecular gradient as a list of x,y,z components for each atom (symbol)
    """
    obj = None
    gradString = []
    if (path_to_file != "" and path_to_file != None): 
        gradString = get_last_molecular_gradient(path_to_file)
    else:
        obj = None
    if gradString == None:
        return None
    obj = get_infoGradient_from_gradString(gradString)
    return obj
    
def get_infoGradient_from_gradString(gradString):
    """return a matrix form of the gradient, its max/min absolute elements and RMS norm.
    Keyword arguments:
    gradString -- the molecular gradient as a list of x,y,z components for each atom (symbol)
    """
    if (gradString== None or gradString==[]):
        return None
    matGrad  = np.array([[float(line[key]) for key in ['x','y','z']] for line in gradString])
    gradient = [[ line['atom'], np.array([float(line[key]) for key in ['x','y','z']]) ] for line in gradString]
    absGrad = np.absolute(matGrad)
    nbAtom = len(absGrad)
    obj = {}
    obj['matGrad']  = matGrad
    obj['gradient'] = gradient
    obj['maxGrad']  = np.amax(absGrad)
    obj['minGrad']  = np.amin(absGrad)
    obj['rmsGrad']  = math.sqrt((sum( [x*x for x in absGrad.flatten()]))/(3.*nbAtom))
    return obj
    

def get_last_molecular_gradient(path_to_file =""):
    isFile = os.path.isfile(path_to_file.strip())
    if isFile == False:
        print "Path to file is not correct: ",path_to_file
        return None
    else:
        # try finding the last "Molcular gradient"
	out = ""
	try:
            cmd= 'sed -n "/Molecular gradient/,/RMS gradient/p" '+path_to_file.strip()
            out1 = subproc.check_output(cmd, shell=True)
            if (out1==""):
                return None
            out2=out1.rsplit('-----------------------', 1)[1]
            out3=out2.rsplit('RMS gradient norm', 1)[0]
            out = [line.strip() for line in out3.split('\n') if line.strip() != '']
	except:
            print "Not able to extract the molecular gradient from this file:\n", path_to_file
            return None
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





# ============================================================================ #
# Testing
# ============================================================================ #
if __name__ == "__main__":
    path_to_file = "./files/lsdalton_files/lsdalton20140924_geomOpt-b3lyp_Vanlenthe_6-31G_df-def2_Histidine_2CPU_16OMP_2014_10_28T1007.out"
    #path_to_file = "./files/lsdalton_files/lsdalton20140924_b3lyp_gradient_ADMM2_6-31Gs_df-def2_3-21G_Histidine_8CPU_16OMP_2014_11_17T1502.out"
    #path_to_file = "/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_6-31Gs/lsdalton20140924_geomOpt-b3lyp_Vanlenthe_6-31Gs_df-def2_Histidine_8CPU_16OMP_2014_11_13T1203.out"
    # grad = get_last_molecular_gradient(path_to_file.strip())
    # gradInfo = get_infoGradient_from_gradString(grad)
    # print gradInfo.keys()
    # print "\nExtracting gradient from:\n  %r\n" % (path_to_file)
    # print "gradient informations:\n  RMS norm: %e\n  Max Abs:  %e\n  Min Abs:  %e" % (gradInfo['rmsGrad'],gradInfo['maxGrad'],gradInfo['minGrad'])
    # print gradInfo['matGrad']

   
    path_to_file = "/home/ctcc2/Documents/CODE-DEV/parse-LSDALTON/src/files/lsdalton_files/lsdalton20140924_b3lyp_gradient_ADMM2_6-31Gs_df-def2_3-21G_Histidine_8CPU_16OMP_2014_11_17T1502.out"
    path_to_file = "/home/ctcc2/Documents/CODE-DEV/parse-LSDALTON/src/files/lsdalton_files/lsdalton20140924_geomOpt-b3lyp_Vanlenthe_6-31G_df-def2_Histidine_2CPU_16OMP_2014_10_28T1007.out"
    # print get_energy_contribution_firstNuclearRepulsion(path_to_file)    
    # print get_energy_contribution_lastNuclearRepulsion(path_to_file)    
    #print path_to_file
    str_mol1 = get_input_MOL_string(path_to_file)
    #obj = parse_input_MOL_string(str_mol1)
    obj = parse_input_MOL_string_atomCoord(str_mol1)
    #print parse_input_MOL_string_BASIS(str_mol1)

    #str_molOpt1 =  get_optmized_MOL_string(path_to_file)
    #parse_optimized_MOL_string_atomCoord(str_molOpt1)


    molInputDalton = parse_molecule_input(path_to_file)
    #print molInputDalton
    #print molInputDalton.nbAtomsInMolecule

    #str_molOpt1 =  get_optmized_MOL_string(path_to_file)
    #print str_molOpt1
    molOptimized = parse_molecule_optimized(path_to_file)
    print molOptimized.getContent_format_XYZ()