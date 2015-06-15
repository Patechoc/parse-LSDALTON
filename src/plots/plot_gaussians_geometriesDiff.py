#!/usr/bin/env python

import sys, os
from datetime import date
import re
#import numpy as np
#import subprocess as subproc
import configFile
import read_LSDALTON_output as readLS
import xyz2molecule as xyz
import topologyDiff as topD
import normalDistribution
#import compare_LSDALTON_outputs as compLS



def run():
    inputs = configFile.get_inputs("Topology differences between various optimized geometries of Valinomycin (cc-pVTZ)")

    today = date.today()
    today_str = today.isoformat()
    mol_list   = inputs.mol_list
    basisPatterns = [bas['pattern'] for bas in inputs.basisSets]
    #dalRef_noDF      = [dal for dal in inputs.dal_list if dal['abrev'] == 'LinK-noDF']

    pattern_LinK = re.compile("LinK")
    dals = [dal for dal in inputs.dal_list if (dal['abrev'] != 'LinK-noDF' and
                                               pattern_LinK.match(dal['abrev']))]
    #print dals
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
    ### get LSDALTON output file on the disk given the inputs
    #print "Inputs:\n",  inputs
    dalRef_noDF      = [dal for dal in inputs.dal_list if dal['abrev'] == 'LinK-noDF'][0]
    path_to_fileRefOut = ""
    path_to_file2Out = path_to_fileRefOut
    path_to_fileRefXYZ = ""
    path_to_file2XYZ   = ""

    filenames = []
    #     filenames = ["valinomycin_geomOpt_DFT-b3lyp_6-31Gs_ADMM2-KT3X_3-21G.out",
    #                  #             "valinomycin_geomOpt_DFT-b3lyp_6-31Gs_ADMM2-PBEX_3-21G.out",
    #                  #             "valinomycin_geomOpt_DFT-b3lyp-noDF_6-31Gs.out",
    #                  #             "valinomycin_geomOpt_DFT-b3lyp_6-31Gs.out",
    #                  #             "valinomycin_geomOpt_DFT-b3lyp_cc-pVTZ_ADMM2-KT3X_3-21G.out",
    #                  #             "valinomycin_geomOpt_DFT-b3lyp_cc-pVTZ_ADMM2-PBEX_3-21G.out",
    #                  "valinomycin_geomOpt_DFT-b3lyp-noDF_cc-pVTZ.out",
    #                  "valinomycin_geomOpt_DFT-b3lyp_cc-pVTZ.out"]
    for molName in inputs.mol_list:
        for dal in inputs.dal_list:
            for basis in inputs.basisSets:
                filenameRefOut = "_".join([molName,
                                           dalRef_noDF["pattern"],
                                           basis["pattern"]]) + ".out"
                #print dalRef_noDF['path_to_files']
                #print filenameRefOut
                path_to_fileRefOut = dalRef_noDF['path_to_files']+"/" + filenameRefOut
                filenames.append("_".join([molName,
                                           dal["pattern"],
                                           basis["pattern"]]) + ".out")

    ### convert the optimized geometries of the LSDALTON outputs into .XYZ files
    path = "/home/ctcc2/Documents/CODE-DEV/xyz2top/xyz2top/tests/files/"
    for filename in filenames:
        molOptimized = readLS.parse_molecule_optimized(path + filename)
        [filepath, extension] = os.path.splitext(path + filename)
        #   print molOptimized
        xyzStr = molOptimized.getContent_format_XYZ()
        #print xyz
        path_to_file2XYZ = filepath +".xyz"
        with open(path_to_file2XYZ, 'w') as outfile:
            outfile.write(xyzStr)

    ### extract and compare the topologies to get statistics
    path_to_fileRefXYZ = os.path.splitext(path_to_fileRefOut)[0] + ".xyz"
    molecule1 = xyz.parse_XYZ(path_to_fileRefXYZ)
    path = "/home/ctcc2/Documents/CODE-DEV/xyz2top/xyz2top/tests/files/"
    for molName in inputs.mol_list:
        for dal in inputs.dal_list:
            for basis in inputs.basisSets:
                filename = "_".join([molName, dal["pattern"], basis["pattern"]]) + ".out"
                [filepath, extension] = os.path.splitext(path + filename)
                path_to_file2XYZ = filepath +".xyz"
                molecule2 = xyz.parse_XYZ(path_to_file2XYZ)
                diff = topD.topologyDiff(molecule1, molecule2, covRadFactor=1.3)
                #print diff
                newComparison = {
                    'molName'      : molName,
                    'dalAbrev'     : dal['abrev'],
                    'basisReg'     : basis['abrev'],
                    'filename'     : filename.split(".")[0],
                    'shortnameRef' : molecule1.shortname,
                    'shortnameMol2': molecule2.shortname,
                    'statsError':diff,
                }
                results.append(newComparison)
    return results


def generate_plots(inputs, results):
    ### plot error in bonds, angles and dihedrals on the same plot for LinK with/without density-fitting
    print inputs
    #import pprint
    #pprint.pprint(results)
    gaussians = []

    for res in results:
        title = "Bond distance deviation from the reference (LinK-noDF/{}) for geometry optimized {}.".format(res['basisReg'], res['molName'])
        if res['dalAbrev'] != 'LinK-noDF':
            #print res['statsError']
            title = "Bond distance diff. for {} against LinK-noDF as reference ({})".format(res['molName'], res['basisReg'])
            gaussians.append({'mean':res['statsError'].error_bonds['mean'],
                              'name':"${} \quad ({:.1E}\pm{:.1E} \angstrom))$".format(res['dalAbrev'], res['statsError'].error_bonds['mean'], res['statsError'].error_bonds['variance']),
                              'variance':res['statsError'].error_bonds['variance']})
            print gaussians
#    max_var = max(res['statsError'].error_bonds['variance'],
#                  res['statsError'].error_angles['variance'],
#                  res['statsError'].error_dihedrals['variance'])
    max_var = max([elem['variance'] for elem in gaussians])
    print "max var = {:.5e}".format(max_var)
#    normalDistribution.plot_Matplotlib(gaussians, title, FROM_X=-1.*max_var, TO_X=max_var)
    normalDistribution.plot_Matplotlib(gaussians, title)


#     # [data, layout] = plot_Plotly(gaussians)
#     # fig = Figure(data=data, layout=layout)
#     # plot_url = py.plot(fig, filename='Topology comparisons')


if __name__ == "__main__":
    run()
