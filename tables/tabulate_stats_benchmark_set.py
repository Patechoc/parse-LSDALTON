#!/usr/bin/env python

import sys, os
import numpy as np
import plotly.plotly as py
import subprocess as subproc
import read_LSDALTON_output as readLS
import compare_LSDALTON_outputs as compLS
from plotly.graph_objs import *
import configFile

def run():
    inputs = configFile.get_inputs("ADMM single SCF + gradient error from LinK reference (6-31G*/3-21G and cc-pVTZ/3-21G)")
    mol_list   = inputs.mol_list
    basis_list = [bas['pattern'] for bas in inputs.basisSets]
    ref        = [dal for dal in inputs.dal_list if dal['abrev'] == 'LinK']
    dal_ref    = [{'LinK':dal['pattern']} for dal in ref]
    path_to_ref = ref[0]['path_to_files']

    dals = [dal for dal in inputs.dal_list if dal['abrev'] != 'LinK']
    dal_list   = []
    dal_list.extend( [{'abrev':dal['abrev'], 'pattern':dal['pattern']} for dal in dals] )
    print dal_list[0]
    path_to_dals = dals[0]['path_to_files']


    #results = get_data(mol_list, basis_list, dal_list, dal_ref, path_to_ref, path_to_dals)
    if inputs.doPlot == True:
        generate_table(title, results, today_str)


def run_command_or_exit(cmd):
    try:
        out = subproc.check_output(cmd, shell=True)
    except subproc.CalledProcessError, e:
#        print type(inst)     # the exception instance
#        print inst.args      # arguments stored in .args
#        print inst           # __str__ allows args to be printed directly
        print "Not able to run this command:\n", cmd
        out = None
    return out

def get_data(mol_list, basis_list, dal_list, dal_ref, path_to_ref, path_to_dals):
    results = {}
    combinationAvoided = []
    for regBasisVal in regBasis_list:
        regBasis = regBasisVal.strip()
        results[regBasis] = {} 
        print regBasis
        dal_files = []
        for dalObj in dal_list:
            dft_func = dalObj['abrev'].strip()
            dalPattern = dalObj['pattern'].strip()
            results[regBasis][dft_func] = {} 
            print "\t\t"+dft_func
            file_dal = ""
            for molVal in mol_list:
                mol  = molVal.strip()
                print "\t"+mol
                file_ref = ""
                cmd= "ls "+ path_to_ref+"/lsd*"+dal_ref[0]['LinK']+"*"+regBasis+"*"+mol+"*.out"
                file_ref = run_command_or_exit(cmd)
                #if file_ref != None:
                #    print "\t\t"+file_ref
                
                cmd= "ls "+ path_to_dals+"/lsd*"+dalPattern+"*"+regBasis+"*"+mol+"*.out"
                file_dal = run_command_or_exit(cmd)
                #if file_dal != None:
                #    print "\t\t"+file_dal

                ## compare gradient of reference with ADMM
                #print file_ref
                diffGrad = compLS.get_compareInfoGradients(file_ref, file_dal)
                #print diffGrad
                if diffGrad != None:
                    results[regBasis][dft_func][mol] =  np.absolute(diffGrad['matDiffGrad'].flatten())
                else:
                    combinationAvoided.append([regBasis,dft_func,mol])
    print "Combinations avoided:\n"
    print "\n".join(["\t".join(combi) for combi in combinationAvoided])
    return results


def generate_table(title, results, today_str):
    myObjArray=[{'FAMILY NAME':'Doe', 'FIRST NAME':'John', 'AGE':'35', 'NATIONALITY':'american', 'License':'B'},
                {'FAMILY NAME':'Merlot', 'FIRST NAME':'Patrick', 'AGE':'35', 'NATIONALITY':'french', 'License':'B'},
                {'FAMILY NAME':'Obama', 'FIRST NAME':'Barak', 'AGE':'62', 'NATIONALITY':'american', 'License':'B'},
                {'FAMILY NAME':'Hollande', 'FIRST NAME':'Francois', 'AGE':'64', 'NATIONALITY':'french', 'License':'B'}]
    newFile = libCSV.write_arrayOfObjects_to_csv(myObjArray, './files/writeObjArray.csv', delimiterW=',', quotecharW='"')

def generate_boxplot(titre, results, mol_list, today_str):
    ## DATA TO PLOT
    #y0 = np.random.randn(50)
    #y1 = np.random.randn(50)+1

    myColors = get_colors()
    traceFunc = {}
    for regbase in results.keys():
        traces = np.array([])
        numFunc = 0
        yFunc = np.array([])
        xFunc = np.array([])
        for func in results[regbase].keys():
            numFunc = numFunc+1
            #for mol in results[regbase][func].keys():
            for mol in [m for m in mol_list if m in results[regbase][func].keys()]:
                elemsPerMol = results[regbase][func][mol] ### elements of grad. diff
                xFunc = np.append(xFunc,[mol for elem in elemsPerMol])
                yFunc = np.append(yFunc,[elemsPerMol])
                traceFunc[func] = Box(y = yFunc,    ### diffGrad elements
                                      x = xFunc,   ### elements grouped on the same molecule
                                      name=func, ### ADMM functional combined for this regBasis set choice
                                      marker=Marker(color=myColors[numFunc%len(myColors)]),
                                      boxpoints='all',
                                      jitter=0.4,
                                      pointpos=-0.0
                                  )
            traces = np.append(traces,traceFunc[func])
            data = Data(traces)
    #print traceFunc['OPTX']
    layout = Layout(
        title=titre, # ('+today_str+')',
        #xaxis=XAxis(
            #title='set of molecules',
            # titlefont=Font(
            #     family='Courier New, monospace',
            #     size=18,
            #     color='#7f7f7f'
            # )
        #),
        yaxis=YAxis(
            title='Abs. errors in molecular gradient',
            zeroline=False,
            # titlefont=Font(
            #     family='Courier New, monospace',
            #     size=18,
            #     color='#7f7f7f'
            # )
            type='log',
            autorange=True,
            exponentformat='power',
        ),
        boxmode='group',
    )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='Gradient differences')



if __name__ == "__main__":
    run()
