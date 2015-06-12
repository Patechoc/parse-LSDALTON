#!/usr/bin/env python

import sys, os
from datetime import date
import re
#import numpy as np
#import plotly.plotly as py
#from plotly.graph_objs import *
#import subprocess as subproc
import configFile
#import read_LSDALTON_output as readLS
#import compare_LSDALTON_outputs as compLS



def run():
    inputs = configFile.get_inputs("Topology differences between various optimized geometries of Valinomycin (cc-pVTZ)")

    today = date.today()
    today_str = today.isoformat()
    mol_list   = inputs.mol_list
    basisPatterns = [bas['pattern'] for bas in inputs.basisSets]
    ref_noDF      = [dal for dal in inputs.dal_list if dal['abrev'] == 'LinK-noDF']

    pattern_LinK = re.compile("LinK")
    dals = [dal for dal in inputs.dal_list if (dal['abrev'] != 'LinK-noDF' and
                                               pattern_LinK.match(dal['abrev']))]
    print dals
    results = get_data(inputs)
    #if inputs.doPlot == True:
    #    generate_plots(inputs.title, results, mol_list, today_str)

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
    results = {}
    print inputs
    path_to_file1 = "/home/ctcc2/Documents/CODE-DEV/xyz2top/xyz2top/tests/files/valinomycin_geomOpt_DFT-b3lyp_cc-pVTZ.xyz"
    path_to_file2 = "/home/ctcc2/Documents/CODE-DEV/xyz2top/xyz2top/tests/files/valinomycin_geomOpt_DFT-b3lyp-noDF_cc-pVTZ.xyz"
    import xyz2molecule as xyz
    molecule1 = xyz.parse_XYZ(path_to_file1)
    molecule2 = xyz.parse_XYZ(path_to_file2)
    import topologyDiff as topD
    diff = topD.topologyDiff(molecule1, molecule2, covRadFactor=1.3)
    print diff
    return results


def generate_plots(titre, results, mol_list, today_str):
    myColors = get_colors()
    # gaussians = [{'mean':0., 'variance':0.2},
    #              {'mean':0., 'variance':1.},
    #              {'mean':0., 'variance':5.},
    #              {'mean':-2., 'variance':0.5}]
    # plot_Matplotlib(gaussians)

    # [data, layout] = plot_Plotly(gaussians)
    # fig = Figure(data=data, layout=layout)
    # plot_url = py.plot(fig, filename='Topology comparisons')


if __name__ == "__main__":
    run()
