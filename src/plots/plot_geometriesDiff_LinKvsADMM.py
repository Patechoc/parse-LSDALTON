#!/usr/bin/env python

import sys, os
from datetime import date
import re
#import numpy as np
import subprocess as subproc
import configFile
import read_LSDALTON_output as readLS
import xyz2molecule as xyz
import topologyDiff as topD
import normalDistribution
import matplotlib.pyplot as plt
#import compare_LSDALTON_outputs as compLS



def run():
    inputs = configFile.get_inputs("Topology deviations due to density-fitting {Valinomycin, cc-pVTZ}")
    results = get_data(inputs)
    if inputs.doPlot == True:
        generate_plots_DensityFitting(inputs, results)

def get_colors():
    bleu   = "rgb( 31,119,180)" ## "color":"rgb(54,144,192)",
    orange = "rgb(255,127, 14)"
    vert   = "rgb( 44,160, 40)"
    rouge  = "rgb(214, 39, 40)"
    violet = "rgb(148,103,189)"
    cian   = "rgb(  0,204,204)"
    colors = [bleu, orange, vert, cian, rouge, violet]
    return colors


def run_command_or_exit(cmd):
    try:
        out = subproc.check_output(cmd, shell=True)
    except subproc.CalledProcessError, e:
        print "Not able to run this command:\n", cmd
        out = None
    return out

def get_data(inputs):
    results = []
    today = date.today()
    today_str = today.isoformat()
    ### get LSDALTON output file on the disk given the inputs
    print "Inputs:\n",  inputs

    ## given molecule, basisReg
    # dals = [dal for dal in inputs.dal_list if (dal['abrev'] != 'LinK-noDF' and
    #                                            pattern_LinK.match(dal['abrev']))]

    basisReg_list = [bas for bas in inputs.basisSets if bas['type']=='regBasis']
    basisAux_list = [bas for bas in inputs.basisSets if bas['type']=='auxBasis']
    for str_mol in inputs.mol_list:
        print "MOL: ",str_mol
        for regBas in basisReg_list:
            print "\tREG BASIS:",regBas

            ## TO SHOW ON THE SAME PLOT
            ## reference = LinK+noDF
            refDal = [dal for dal in inputs.dal_list if dal['abrev']=='LinK-noDF'][0]
            print "\tDAL_REF:",refDal['abrev']
            dals   = [dal for dal in inputs.dal_list if dal['abrev']!='LinK-noDF']
            path_to_RefOut = refDal['path_to_files']
            grepRefOut = path_to_RefOut + "/lsdalton*" + "".join([refDal["pattern"],"*",
                                                                   regBas['pattern'],"*",
                                                                   str_mol]) + "*.out"

            cmd = "ls " + grepRefOut
            res_cmd = run_command_or_exit(cmd).strip().split("\n")
            pathToFile_RefOut = ""
            if (len(res_cmd) != 1):
                sys.exit("no files or too many fitting this command: "+cmd)
            else:
                pathToFile_RefOut= res_cmd[0]
            pathToXYZ = "./temp/"
            cmd = "mkdir -p " + pathToXYZ
            res_cmd = run_command_or_exit(cmd)

            molOptimREF = readLS.parse_molecule_optimized(pathToFile_RefOut)
            [filepath, extension] = os.path.splitext(os.path.basename(pathToFile_RefOut))
            xyzStr = molOptimREF.getContent_format_XYZ()
            path_to_fileRefXYZ = pathToXYZ + filepath +".xyz"
            with open(path_to_fileRefXYZ, 'w') as outfile:
                outfile.write(xyzStr)
            moleculeREF = xyz.parse_XYZ(path_to_fileRefXYZ)

            ## compared Ref topology to: LinK+DF with basisAux (df-def2 or cc-pVTZdenfit)
            for dal in dals:
                print "\t\tDAL:",dal['abrev']
                for aux in basisAux_list:
                    # compare topo, store results to be returned
                    print "\t\t\tAUX:",aux['abrev']
                    path_to_out = dal['path_to_files']
                    grepOut = path_to_out + "/lsdalton*" + "".join([dal["pattern"],"*",
                                                                       regBas['pattern'],"*",
                                                                       aux['pattern'],"*",
                                                                       str_mol]) + "*.out | grep -v "+refDal["pattern"]
                    cmd = "ls " + grepOut
                    res_cmd = run_command_or_exit(cmd).strip().split("\n")
                    pathToFile_out = ""
                    if (len(res_cmd) != 1):
                        sys.exit("no files or too many fitting this command: " + cmd)
                    else:
                        pathToFile_out = res_cmd[0]
                    molOptimXYZ = readLS.parse_molecule_optimized(pathToFile_out)
                    [filepath, extension] = os.path.splitext(os.path.basename(pathToFile_out))
                    xyzStr = molOptimXYZ.getContent_format_XYZ()
                    path_to_fileXYZ = pathToXYZ + filepath +".xyz"
                    with open(path_to_fileXYZ, 'w') as outfile:
                        outfile.write(xyzStr)

                    ### extract and compare the topologies to get statistics
                    molecule = xyz.parse_XYZ(path_to_fileXYZ)
                    diff = topD.topologyDiff(moleculeREF, molecule)
                    #print diff
                    newComparison = {
                        'molName'      : str_mol,
                        'basisREG'     : regBas,
                        'dalREF'       : refDal,
                        'fileOutREF' : pathToFile_RefOut,
                        'fileOut2'   : pathToFile_out,
                        'fileXYZREF' : path_to_fileRefXYZ,
                        'fileXYZ2'   : path_to_fileXYZ,
                        'dal2'         : dal,
                        'basisAux'     : aux,
                        'diffTopoError': diff,
                    }
                    results.append(newComparison)
    return results


def generate_plots_DensityFitting(inputs, results):
    plt.close('all')
    ### plot error in bonds, angles and dihedrals on the same plot for LinK with/without density-fitting
    print inputs
    #import pprint
    #pprint.pprint(results)
    bonds = []
    angles = []
    dihedrals = []
    basisReg_list = [bas for bas in inputs.basisSets if bas['type']=='regBasis']
    for str_mol in [mols for mols in inputs.mol_list if mols=='valinomycin']:
        for regBas in basisReg_list:
            for res in [subres for subres in results if subres['molName']==str_mol and subres['basisREG']==regBas]:
                title = "/{} ({}, ref=LinK without DF)".format(res['molName'],regBas['abrev'])
                titleBonds = "Bond deviations"+ title
                titleAngles = "Angle deviations"+ title
                titleDihedrals = "Dihedral deviations"+ title
                print res['diffTopoError']
                if True:
                    ######### BONDS ######### 
                    name = "{}/{}".format(res['dal2']['abrev'],
                                          res['basisAux']['abrev'])
                    #name += " $(\mu={:.1E}\pm{:.1E} \, \AA )$".format(res['diffTopoError'].error_bonds['mean'], res['diffTopoError'].error_bonds['variance'])
                    bonds.append({
                        'mean':res['diffTopoError'].error_bonds['mean'],
                        'variance':res['diffTopoError'].error_bonds['variance'],
                        'basisReg':res['basisREG'],
                        'name':name})

                    ######### ANGLES ######### 
                    name = "{}/{}".format(res['dal2']['abrev'],
                                          res['basisAux']['abrev'])
                    #name += " $(\mu={:.1E}\pm{:.1E} ^\circ )$".format(res['diffTopoError'].error_angles['mean'], res['diffTopoError'].error_amgles['variance'])
                    angles.append({
                        'mean':res['diffTopoError'].error_angles['mean'],
                        'variance':res['diffTopoError'].error_angles['variance'],
                        'basisReg':res['basisREG'],
                        'name':name})

                    ######### DIHEDRAL ANGLES ######### 
                    name = "{}/{}".format(res['dal2']['abrev'],
                                          res['basisAux']['abrev'])
                    #name += " $(\mu={:.1E}\pm{:.1E} ^\circ )$".format(res['diffTopoError'].error_dihedrals['mean'], res['diffTopoError'].error_dihedrals['variance'])
                    dihedrals.append({
                        'mean':res['diffTopoError'].error_dihedrals['mean'],
                        'variance':res['diffTopoError'].error_dihedrals['variance'],
                        'basisReg':res['basisREG'],
                        'name':name})

            #    normalDistribution.plot_Matplotlib(bonds, title, FROM_X=-1.*max_var, TO_X=max_var)
            normalDistribution.plot_Plotly(bonds, titleBonds)
            normalDistribution.plot_Plotly(angles, titleAngles)
            normalDistribution.plot_Plotly(dihedrals, titleDihedrals)

            normalDistribution.plot_Matplotlib(bonds, titleBonds)
            normalDistribution.plot_Matplotlib(angles, titleAngles)
            normalDistribution.plot_Matplotlib(dihedrals, titleDihedrals)
            plt.show()

if __name__ == "__main__":
    run()
