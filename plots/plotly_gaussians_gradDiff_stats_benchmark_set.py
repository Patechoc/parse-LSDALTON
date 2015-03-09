#!/usr/bin/env python

import sys, os
import numpy as np
import plotly.plotly as py
import subprocess as subproc
import read_LSDALTON_output as readLS
import compare_LSDALTON_outputs as compLS
from plotly.graph_objs import *
import configFile
import scipy.stats as stats
import pylab as pl


def run():
    generate_test_plot()

def generate_test_plot():
    h = sorted([186, 176, 158, 180, 186, 168, 168, 164, 178, 170, 189, 195, 172,
                187, 180, 186, 185, 168, 179, 178, 183, 179, 170, 175, 186, 159,
                161, 178, 175, 185, 175, 162, 173, 172, 177, 175, 172, 177, 180])  #sorted
    
    fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
    #pl.plot(h,fit,'-')
    #pl.hist(h,normed=True)      #use this to draw histogram of your data
    #pl.show() 
    
    trace1 = Scatter(
        x=h,
        y=fit,
        name="errors",
        marker=Marker(size=12),
        line=Line(dash='dot',     # dot, longdashdot
                  shape='spline', # linear or spline
                  color='rgb(204, 0, 0)',
                  width=3),
        xsrc='cimar:167:3db457',
        ysrc='cimar:167:98813d'
    )
    data = Data([trace1])
    layout = Layout(
        title='Click to enter Plot title',
        titlefont=Font(
            family='',
            size=0,
            color=''
        ),
    font=Font(
        family='"Open sans", verdana, arial, sans-serif',
        size=12,
        color='#444'
    ),
    showlegend=False,
        autosize=True,
        width=1522,
        height=579,
        xaxis=XAxis(
            title='Click to enter X axis title',
            titlefont=Font(
                family='',
                size=0,
                color=''
            ),
        range=[0.7482472399065194, 5],
            domain=[0, 1],
            type='linear',
            rangemode='normal',
            autorange=True,
            showgrid=True,
            zeroline=True,
            showline=False,
            autotick=True,
            nticks=0,
            ticks='',
            showticklabels=True,
            tick0=0,
            dtick=0.5,
            ticklen=5,
            tickwidth=1,
            tickcolor='#444',
            tickangle='auto',
            tickfont=Font(
                family='',
                size=0,
                color=''
            ),
        exponentformat='B',
            showexponent='all',
            mirror=False,
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='#444',
            zerolinewidth=1,
            linecolor='#444',
            linewidth=1,
            anchor='y',
            overlaying=False,
            position=0
        ),
    yaxis=YAxis(
        title='Click to enter Y axis title',
        titlefont=Font(
            family='',
            size=0,
            color=''
        ),
        range=[4.333333333333333, 17.666666666666668],
        domain=[0, 1],
        type='linear',
        rangemode='normal',
        autorange=True,
        showgrid=True,
        zeroline=True,
        showline=False,
        autotick=True,
        nticks=0,
        ticks='',
        showticklabels=True,
        tick0=0,
        dtick=2,
        ticklen=5,
        tickwidth=1,
        tickcolor='#444',
        tickangle='auto',
        tickfont=Font(
            family='',
            size=0,
            color=''
        ),
        exponentformat='B',
        showexponent='all',
        mirror=False,
        gridcolor='rgb(255, 255, 255)',
        gridwidth=1,
        zerolinecolor='#444',
        zerolinewidth=1,
        linecolor='#444',
        linewidth=1,
        anchor='x',
        overlaying=False,
        position=0
    ),
    legend=Legend(
        x=1.02,
        y=1,
        traceorder='normal',
        font=Font(
            family='',
            size=0,
            color=''
        ),
        bgcolor='#fff',
        bordercolor='#444',
        borderwidth=0,
        xanchor='left',
        yanchor='top'
    ),
    margin=Margin(
        l=80,
        r=80,
        b=80,
        t=100,
        pad=0,
        autoexpand=True
    ),
    paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        hovermode='x',
        dragmode='zoom',
        separators='.,',
        barmode='group',
        bargap=0.2,
        bargroupgap=0,
        boxmode='overlay',
        boxgap=0.3,
        boxgroupgap=0.3,
        hidesources=False
    )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='test error distributions')

    
def run1():
    inputs = configFile.get_inputs("ADMM2/ADMMS (6-31G*/3-21G) single gradient deviation from geom. opt. ref. (6-31G*)")
    
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
    results = get_data(mol_list, basis_list, dal_list, dal_ref, path_to_ref, path_to_dals)
    if inputs.doPlot == True:
        generate_boxplot(title, results, mol_list, today_str)
    

def get_colors():
    bleu  ="rgb( 31,119,180)" ## "color":"rgb(54,144,192)",
    orange="rgb(255,127, 14)"
    vert  ="rgb( 44,160, 40)"
    rouge ="rgb(214, 39, 40)"
    violet="rgb(148,103,189)"
    colors=[bleu, orange, vert, rouge, violet]
    return colors


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
    for basisVal in basis_list:
        basis = basisVal.strip()
        results[basis] = {} 
        print basis
        dal_files = []
        for dalObj in dal_list:
            dft_func = dalObj['abrev'].strip()
            dalPattern = dalObj['pattern'].strip()
            results[basis][dft_func] = {} 
            print "\t\t"+dft_func
            file_dal = ""
            for molVal in mol_list:
                mol  = molVal.strip()
                print "\t"+mol
                file_ref = ""
                cmd= "ls "+ path_to_ref+"/lsd*"+dal_ref[0]['LinK']+"*"+basis+"*"+mol+"*.out"
                file_ref = run_command_or_exit(cmd)
                #if file_ref != None:
                #    print "\t\t"+file_ref
                
                cmd= "ls "+ path_to_dals+"/lsd*"+dalPattern+"*"+basis+"*"+mol+"*.out"
                file_dal = run_command_or_exit(cmd)
                #if file_dal != None:
                #    print "\t\t"+file_dal

                ## compare gradient of reference with ADMM
                #print file_ref
                diffGrad = compLS.get_compareInfoGradients(file_ref, file_dal)
                #print diffGrad
                if diffGrad != None:
                    results[basis][dft_func][mol] =  np.absolute(diffGrad['matDiffGrad'].flatten())
                else:
                    combinationAvoided.append([basis,dft_func,mol])
    print "Combinations avoided:\n"
    print "\n".join(["\t".join(combi) for combi in combinationAvoided])
    return results


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
                                      name=func, ### ADMM functional combined for this basis set choice
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
