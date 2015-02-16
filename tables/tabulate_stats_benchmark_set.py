#!/usr/bin/env python

import sys, os
import numpy as np
import subprocess as subproc
import read_LSDALTON_output as readLS
import compare_LSDALTON_outputs as compLS
import configFile
import statistics as stats
import lib_spreadsheet as libCSV

def run():
    inputs = configFile.get_inputs("ADMM single SCF + gradient error from LinK reference (6-31G*/3-21G and cc-pVTZ/3-21G)")
    results = get_data(inputs)
    pathOutput = "/home/ctcc2/Documents/CODE-DEV/parse-LSDALTON/files/tables/"
    filename = "ADMM_gradient_error.csv"
    if inputs.doPlot == True:
        generate_table(inputs, results, pathOutput+filename)


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

def get_data(inputs):
    results = {}
    combinationAvoided = []
    mol_list   = inputs.mol_list ## [molecule_name]
    basis_list = [bas['pattern'] for bas in inputs.basisSets]  ### 6-31Gs
    ref        = [dal for dal in inputs.dal_list if dal['abrev'] == 'LinK'] ### {abrev, path, pattern}
    
    dal_ref    = [{'LinK':dal['pattern']} for dal in ref] ## [{'LinK':pattern}]
    path_to_ref = ref[0]['path_to_files']

    dals = [dal for dal in inputs.dal_list if dal['abrev'] != 'LinK'] ## [{abrev, path, pattern}, {abrev, path, pattern}, ...]
    list_func = list(set([dal['abrev'].split('-')[1] for dal in dals]))
    list_ADMM = list(set([dal['abrev'].split('-')[0] for dal in dals]))

    dal_list   = []
    dal_list.extend( [{'abrev':dal['abrev'], 'pattern':dal['pattern']} for dal in dals] )
    path_to_dals = dals[0]['path_to_files']

    for regBasisVal in basis_list:
        regBasis = regBasisVal.strip()
        #print regBasis
        results[regBasis] = {} 
        for func in list_func:
            results[regBasis][func] = {} 
            for admm in list_ADMM:
                dal_abrev = admm+"-"+func
                dalPattern = [dal['pattern'] for dal in dal_list if dal['abrev'] == dal_abrev][0]
                results[regBasis][func][admm] = {} 
                for molVal in mol_list:
                    mol  = molVal.strip()
                    results[regBasis][func][admm][mol] = {} 
                    cmd= "ls "+ path_to_ref+"/lsd*"+dal_ref[0]['LinK']+"*"+regBasis+"*"+mol+"*.out"
                    file_ref = run_command_or_exit(cmd)
                    # if file_ref != None:
                    #     print "\t\t"+file_ref
                    
                    cmd= "ls "+ path_to_dals+"/lsd*"+dalPattern+"*"+regBasis+"*"+mol+"*.out"
                    file_dal = run_command_or_exit(cmd)
                    # if file_dal != None:
                    #     print "\t\t"+file_dal

                    ## compare gradient of reference with ADMM
                    #print file_ref
                    diffGrad = compLS.get_compareInfoGradients(file_ref, file_dal)
                    #print diffGrad
                    if diffGrad != None:
                        results[regBasis][func][admm][mol] =  stats.matrix( diffGrad['matDiffGrad'] ).get_stats()
                    else:
                        combinationAvoided.append([regBasis, func, admm, mol])
    avoidedCases = "".join(["\t".join(combi) for combi in combinationAvoided])
    if avoidedCases != "":
        print "Combinations avoided:\n"
        print avoidedCases
    return results


def generate_table(inputs, results, path_to_file):
    myObjArray=[{'FAMILY NAME':'Doe', 'FIRST NAME':'John', 'AGE':'35', 'NATIONALITY':'american', 'License':'B'},
                {'FAMILY NAME':'Merlot', 'FIRST NAME':'Patrick', 'AGE':'35', 'NATIONALITY':'french', 'License':'B'},
                {'FAMILY NAME':'Obama', 'FIRST NAME':'Barak', 'AGE':'62', 'NATIONALITY':'american', 'License':'B'},
                {'FAMILY NAME':'Hollande', 'FIRST NAME':'Francois', 'AGE':'64', 'NATIONALITY':'french', 'License':'B'}]
    newFile = libCSV.write_arrayOfObjects_to_csv(myObjArray, path_to_file, delimiterW=',', quotecharW='"')




if __name__ == "__main__":
    run()
