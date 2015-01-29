#!/usr/bin/env python

import sys, os
import numpy as np
import plotly.plotly as py
import subprocess as subproc
import read_LSDALTON_output as readLS
import compare_LSDALTON_outputs as compLS
from datetime import date
from plotly.graph_objs import *


def main():
    today = date.today()
    today_str = today.isoformat()

    mol_list = ['Histidine','Ferrocene']
    basis_list = ['6-31Gs']
    dal_list = [{'abrev':'OPTX', 'pattern':'b3lyp_gradient_ADMM2-OPTX_'},
                {'abrev':'B88X', 'pattern':'b3lyp_gradient_ADMM2_'}]
    dal_ref = [{'LinK':'geomOpt-b3lyp_Vanlenthe_'}]
    path_to_ref = "/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_6-31Gs"
    path_to_dals = path_to_ref
    results = get_data(mol_list, basis_list, dal_list, dal_ref, path_to_ref, path_to_dals)
    generate_plot(results, today_str)
    

def get_colors():
    bleu  ="rgb( 31,119,180)" ## "color":"rgb(54,144,192)",
    orange="rgb(255,127, 14)"
    vert  ="rgb( 44,160, 40)"
    rouge ="rgb(214, 39, 40)"
    violet="rgb(148,103,189)"
    colors=[bleu, orange, vert, rouge, violet]
    return colors


def run_command_or_exit(cmd):
    out = None
    try:
        out = subproc.check_output(cmd, shell=True)
    except Exception as inst:
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst           # __str__ allows args to be printed directly
        print "Not able to open the reference output using:\n", cmd
    return out

def get_data(mol_list, basis_list, dal_list, dal_ref, path_to_ref, path_to_dals):
    results = {}
    for basisVal in basis_list:
        basis = basisVal.strip()
        results[basis] = {} 
        print basis
        for molVal in mol_list:
            mol  = molVal.strip()
            results[basis][mol] = {} 
            print "\t"+mol
            file_ref = ""

            cmd= "ls "+ path_to_ref+"/lsd*"+dal_ref[0]['LinK']+"*"+basis+"*"+mol+"*"
            file_ref = run_command_or_exit(cmd).strip()
            print "\t"+file_ref
            dal_files = []
            for dalObj in dal_list:
                dft_func = dalObj['abrev'].strip()
                dalPattern = dalObj['pattern'].strip()
                print "\t\t"+dft_func
                file_dal = ""
                cmd= "ls "+ path_to_dals+"/lsd*"+dalPattern+"*"+basis+"*"+mol+"*"
                file_dal = run_command_or_exit(cmd).strip()
                print "\t\t"+file_dal

                ## compare gradient of reference with ADMM
                #print file_ref
                diffGrad = compLS.get_compareInfoGradients(file_ref, file_dal)
                #print diffGrad
                results[basis][mol][dft_func] =  diffGrad['matDiffGrad'].flatten()
    return results


def generate_plot(results, today_str):
    ## DATA TO PLOT
    y0 = np.random.randn(50)
    y1 = np.random.randn(50)+1

    trace1 = Box(
        y=y0
    )
    trace4 = Box(
        y=y1,
        x='molecule 2'    
    )

    x = ['molecule 1', 'molecule 1', 'molecule 1', 'molecule 1', 'molecule 1', 
         'molecule 2', 'molecule 2', 'molecule 2', 'molecule 2', 'molecule 2']


    trace1 = Box(
        y=[0.2, 0.2, 0.6, 1.0, 0.5, 0.4, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3], ## diff. gradient elems 
        x=x,## nb. atoms in molecule, ou molName
        name='KT3X', # ADMM functional combined with basis set choice
        marker=Marker(
            color='#3D9970'),
        boxpoints='all',
        jitter=0.4,
        pointpos=-0.0
    )
    trace2 = Box(
        y=[0.6, 0.7, 0.3, 0.6, 0.0, 0.5, 0.7, 0.9, 0.5, 0.8, 0.7, 0.2],
        x=x,
        name='B88X',
        marker=Marker(
            color='#FF4136'
        ),
        boxpoints='all',
        jitter=0.4,
        pointpos=-0.0

    )
    trace3 = Box(
        y=[0.1, 0.3, 0.1, 0.9, 0.6, 0.6, 0.9, 1.0, 0.3, 0.6, 0.8, 0.5],
        x=x,
        name='OPTX',
        marker=Marker(
            color='#FF851B'
        ),
        boxpoints='all',
        jitter=0.4,
        pointpos=-0.0
    )



    # trace2 = Scatter(
    #     x=[0, 1, 2], # nb-atoms / name molecule
    #     y=[3, 4, 6], # avg. difference over gradient difference
    #     mode = 'markers',
    #     name = 'monTrace2',
    #     error_y=ErrorY(
    #         type='data',
    #         array=[1, 2, 3], # RMS norm
    #         visible=True),
    #     marker=Marker(
    #         #color='#85144B',
    #         size=8, )
    # )

    data = Data([trace1, trace2, trace3])

    layout = Layout(
        title='Impact on molecular gradient'+today_str,
        xaxis=XAxis(
            title='set of molecules',
            # titlefont=Font(
            #     family='Courier New, monospace',
            #     size=18,
            #     color='#7f7f7f'
            # )
        ),
        yaxis=YAxis(
            title='Errors in molecular gradient',
            zeroline=False,
            # titlefont=Font(
            #     family='Courier New, monospace',
            #     size=18,
            #     color='#7f7f7f'
            # )
        ),
        boxmode='group',
    )


    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='Gradient differences')



if __name__ == "__main__":
    main()

