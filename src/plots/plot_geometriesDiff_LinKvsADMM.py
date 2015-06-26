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
    title = "Topology deviations - ADMM"
    inputs = configFile.get_inputs(title)
    results = get_data(inputs)
    if inputs.doPlot == True:
        generate_plots(inputs, results)

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

    basisReg_list  = [bas for bas in inputs.basisSets if bas['type']=='regBasis']
    basisAux_list  = [bas for bas in inputs.basisSets if bas['type']=='auxBasis']
    basisADMM_list = [bas for bas in inputs.basisSets if bas['type']=='admmBasis']
    for str_mol in inputs.mol_list:
        print "MOL: ",str_mol
        for regBas in basisReg_list:
            print "\t\tREG BASIS:",regBas
            for aux in basisAux_list:
                print "\tAUX:",aux['abrev']
                ## TO SHOW ON THE SAME PLOT
                ## reference = LinK-df vs ADMM
                refDal = [dal for dal in inputs.dal_list if dal['abrev']=='LinK'][0]
                print "\t\t\tDAL_REF:",refDal['abrev']
                dals   = [dal for dal in inputs.dal_list if dal['abrev']!='LinK']
                paths_to_RefOut = refDal['path_to_files']
                pathToFile_RefOut = ""
                ind = 0
                res_cmd = None
                while res_cmd == None and ind < len(paths_to_RefOut):
                    #print "\t\tind:",ind
                    path_to_RefOut = paths_to_RefOut[ind]
                    grepRefOut = path_to_RefOut + "/lsdalton*" + "".join([refDal["pattern"],"_",
                                                                          regBas['pattern'],"*",
                                                                          aux['pattern'],"*",
                                                                          str_mol])  + "*.out"

                    cmd = "ls " + grepRefOut
                    res_tmp = run_command_or_exit(cmd)
                    if res_tmp != None:
                        res_cmd = res_tmp.strip().split("\n")
                        pathToFile_RefOut = ""
                        if (len(res_cmd) != 1):
                            sys.exit("no files or too many fitting this command: "+cmd)
                        else:
                            pathToFile_RefOut= res_cmd[0]
                    else:
                        ind = ind + 1
                    #print "\t\t",pathToFile_RefOut

                ### convert dalton output to XYZ format
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
                    print "\t\t\tDAL:",dal['abrev']
                    for admmBas in basisADMM_list:
                        print "\t\t\t\tADMM basis:", admmBas['abrev']
                        path_to_dalOut = dal['path_to_files']
                        pathToFile_out = ""
                        ind = 0
                        res_cmd = None
                        while res_cmd == None and ind < len(path_to_dalOut):
                            #print "\t\t\t\t\tind: ",ind
                            path_to_out = path_to_dalOut[ind]
                            grepOut = path_to_out + "/lsdalton*"\
                                      + "".join([dal["pattern"],"*",
                                                 regBas['pattern'],"*",
                                                 aux['pattern'],"*",
                                                 str_mol]) + "*.out | grep -v " + refDal['pattern']
                            cmd = "ls " + grepOut
                            res_tmp = run_command_or_exit(cmd)
                            if res_tmp != None:
                                res_cmd = res_tmp.strip().split("\n")
                                pathToFile_out = ""
                                if (len(res_cmd) != 1):
                                    sys.exit("no files or too many fitting this command: " + cmd)
                                else:
                                    pathToFile_out = res_cmd[0]
                            else:
                                ind = ind + 1
                            #print "\t\t\t\t\tres_cmd",res_cmd

                        ### convert dalton output to XYZ format
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
                            'molName'    : str_mol,
                            'basisREG'   : regBas,
                            'basisAux'   : aux,
                            'dalREF'     : refDal,
                            'dal2'       : dal,
                            'basisADMM'  : admmBas,
                            'fileOutREF' : pathToFile_RefOut,
                            'fileOut2'   : pathToFile_out,
                            'fileXYZREF' : path_to_fileRefXYZ,
                            'fileXYZ2'   : path_to_fileXYZ,
                            'diffTopoError': diff,
                        }
                        results.append(newComparison)
    return results


def generate_plots(inputs, results):
    plt.close('all')
    ### plot error in bonds, angles and dihedrals on the same plot for LinK with/without density-fitting
    print inputs
    #import pprint
    #pprint.pprint(results)
    basisReg_list = [bas for bas in inputs.basisSets if bas['type']=='regBasis']
    basisAux_list  = [bas for bas in inputs.basisSets if bas['type']=='auxBasis']
    basisADMM_list = [bas for bas in inputs.basisSets if bas['type']=='admmBasis']

    #for str_mol in [mols for mols in inputs.mol_list if mols=='valinomycin']:
    for str_mol in inputs.mol_list:
        print "str_mol: ",str_mol
        for regBas in basisReg_list:
            print "\tregBas: ",regBas
            for aux in basisAux_list:
                print "\t\taux: ",aux
                bonds = []
                angles = []
                dihedrals = []
                for admmBas in basisADMM_list:
                    plt.close('all')
                    print "\t\t\tadmmBas: ",admmBas
                    for res in [subres for subres in results\
                                if subres['molName']==str_mol\
                                and subres['basisAux']==aux\
                                and subres['basisREG']==regBas\
                                and subres['basisADMM']==admmBas]:
                        #print "\t\t\t\tres: ",res
                        title = "/{} x {} (ref=LinK+DF({}))".format(res['molName'],
                                                                    regBas['abrev'],
                                                                    aux['abrev'])
                        titleBonds = "Bond deviations"+ title
                        titleAngles = "Angle deviations"+ title
                        titleDihedrals = "Dihedral deviations"+ title
                        #print res['diffTopoError']
                        if True:
                            ######### BONDS ######### 
                            name = "{}/{}".format(res['dal2']['abrev'],
                                                  res['basisADMM']['abrev'])
                            #name += " $(\mu={:.1E}\pm{:.1E} \, \AA )$".format(res['diffTopoError'].error_bonds['mean'], res['diffTopoError'].error_bonds['variance'])
                            # name = str_mol + "/"+\
                            #        regBas['abrev'] + "/"+\
                            #        aux['abrev'] + "/"+\
                            #        admmBas['abrev']
                            bonds.append({
                                'mean':res['diffTopoError'].error_bonds['mean'],
                                'variance':res['diffTopoError'].error_bonds['variance'],
                                'basisReg':res['basisREG'],
                                'basisAux':res['basisAux'],
                                'dal'     :res['dal2'],
                                'basisADMM':res['basisADMM'],
                                'xUnit':'angstrom',
                                'name':name})

                            ######### ANGLES ######### 
                            #name += " $(\mu={:.1E}\pm{:.1E} ^\circ )$".format(res['diffTopoError'].error_angles['mean'], res['diffTopoError'].error_amgles['variance'])
                            angles.append({
                                'mean':res['diffTopoError'].error_angles['mean'],
                                'variance':res['diffTopoError'].error_angles['variance'],
                                'basisReg':res['basisREG'],
                                'basisAux':res['basisAux'],
                                'dal'     :res['dal2'],
                                'basisADMM':res['basisADMM'],
                                'xUnit':'degree',
                                'name':name})

                            ######### DIHEDRAL ANGLES ######### 
                            #name += " $(\mu={:.1E}\pm{:.1E} ^\circ )$".format(res['diffTopoError'].error_dihedrals['mean'], res['diffTopoError'].error_dihedrals['variance'])
                            dihedrals.append({
                                'mean':res['diffTopoError'].error_dihedrals['mean'],
                                'variance':res['diffTopoError'].error_dihedrals['variance'],
                                'basisReg':res['basisREG'],
                                'basisAux':res['basisAux'],
                                'dal'     :res['dal2'],
                                'basisADMM':res['basisADMM'],
                                'xUnit':'degree',
                                'name':name})

                        #    normalDistribution.plot_Matplotlib(bonds, title, FROM_X=-1.*max_var, TO_X=max_var)
                    # ### PLOTLY
                    normalDistribution.plot_Plotly(bonds,
                                                   titleBonds,
                                                   xLabel=u"Bond deviation (\u212B)")
                    # normalDistribution.plot_Plotly(angles,
                    #                                titleAngles,
                    #                                xLabel=u"Angle deviation (\u00B0)")
                    # normalDistribution.plot_Plotly(dihedrals,
                    #                                titleDihedrals,
                    #                                xLabel=u"Dihedral deviation (\u00B0)")

                    ### MATPLOTLIB
                    #normalDistribution.plot_Matplotlib(bonds, titleBonds)
                    #normalDistribution.plot_Matplotlib(angles, titleAngles)
                    #normalDistribution.plot_Matplotlib(dihedrals, titleDihedrals)
                plt.show()

if __name__ == "__main__":
    run()
