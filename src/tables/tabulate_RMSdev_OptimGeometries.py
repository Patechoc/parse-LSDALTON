#!/usr/bin/env python

import sys, os
import numpy as np
import numpy.testing as npt
import subprocess as subproc
import read_LSDALTON_output as readLS
#import compare_geometries as compGeo
import configFile
import statistics as stats
import lib_spreadsheet as libCSV
import csv

def run():
    inputs = configFile.get_inputs("RMS deviation between optimized geometries (LinK/6-31G* vs LinK/cc-pVTZ)")
    path_to_XYZ = inputs.dal_list[0]['path_to_files']+"/tmp_XYZ"
    if not os.path.exists(path_to_XYZ):
        os.makedirs(path_to_XYZ)
    convert_geometries_to_XYZ_format(inputs, path_to_XYZ)
    # results = get_data(inputs)
    # pathOutput = "/home/ctcc2/Documents/CODE-DEV/parse-LSDALTON/src/files/tables/"
    # filename = "ADMM_gradient_error_6-31Gs.csv"
    # if inputs.doPlot == True:
    #     generate_table(inputs, results, pathOutput+filename)

    # inputs = configFile.get_inputs("ADMM single SCF + gradient error from LinK reference (cc-pVTZ/3-21G)")
    # results = get_data(inputs)
    # pathOutput = "/home/ctcc2/Documents/CODE-DEV/parse-LSDALTON/src/files/tables/"
    # filename = "ADMM_gradient_error_cc-pVTZ.csv"
    # if inputs.doPlot == True:
    #     generate_table(inputs, results, pathOutput+filename)


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


def get_list_functionals(dals):
    funcs = [dal['abrev'].split('-')[1] for dal in dals]
    #list_func = list(set([dal['abrev'].split('-')[1] for dal in dals])) ### unordered list of unique functionals
    list_func = [ v for (i,v) in enumerate(funcs) if v not in funcs[0:i] ] ### keep order of the list with unique functionals
    return list_func

def get_list_ADMM(dals):
    ADMMs = [dal['abrev'].split('-')[0] for dal in dals]
    #list_ADMM = list(set([dal['abrev'].split('-')[0] for dal in dals]))  ### unordered list of unique functionals
    list_ADMM = [ v for (i,v) in enumerate(ADMMs) if v not in ADMMs[0:i] ] ### keep order of the list with unique functionals
    return list_ADMM

def convert_geometries_to_XYZ_format(inputs, path_to_XYZ):
    results = {}
    mol_list   = inputs.mol_list ## [molecule_name]
    basis_list = [bas['pattern'] for bas in inputs.basisSets if bas['pattern']!='cc-pVTZ']  ### 6-31Gs
    basis_list_REF = [bas['pattern'] for bas in inputs.basisSets if bas['pattern']=='cc-pVTZ']  ### cc-pVTZ
    ref        = [dal for dal in inputs.dal_list if dal['abrev'] == 'LinK/cc-pVTZ'] ### {abrev, path, pattern}
    dal_ref    = [{'LinK/cc-pVTZ':dal['pattern']} for dal in ref] ## [{'LinK/cc-pVTZ':pattern}]
    path_to_ref = ref[0]['path_to_files']

    dals = [dal for dal in inputs.dal_list if dal['abrev'] != 'LinK/cc-pVTZ'] ## [{abrev, path, pattern}, {abrev, path, pattern}, ...]
    for dal in dals:
        dalAbrev = dal['abrev']
        print dalAbrev
        dalPattern = dal['pattern']
        results[dalAbrev] = {}
        for molVal in mol_list:
            mol  = molVal.strip()
            print "\t"+mol
            results[dalAbrev][mol] = {}
            ## geom. optim.(LinK) calculation, without ADMM
            ## ex.: ls lsd*geomOpt-b3lyp_Vanlenthe*Histidine*out | grep -v ADMM
            cmd= "ls "+ path_to_ref+"/lsd*"+dal_ref[0]['LinK/cc-pVTZ']+"*"+mol+"*.out  | grep -v ADMM[2,S]"
            file_ref = run_command_or_exit(cmd).strip()
            molXYZ_ref_input    = readLS.parse_molecule_input(file_ref) #.getContent_format_XYZ()
            molXYZ_ref_optimized= readLS.parse_molecule_optimized(file_ref) #.getContent_format_XYZ()
            name_molXYZ_input = dalPattern+"_"+mol+"_input.xyz"
            name_molXYZ_optim = dalPattern+"_"+mol+"_optimized.xyz"
            print name_molXYZ_input
            print name_molXYZ_optim
            with open(path_to_XYZ+"/"+name_molXYZ_input, "w") as text_file:
                text_file.write("{0}".format(molXYZ_ref_input))
            with open(path_to_XYZ+"/"+name_molXYZ_optim, "w") as text_file:
                text_file.write("{0}".format(molXYZ_ref_optimized))

def get_data(inputs):
    results = {}
    combinationAvoided = []
    mol_list   = inputs.mol_list ## [molecule_name]
    basis_list = [bas['pattern'] for bas in inputs.basisSets]  ### 6-31Gs
    ref        = [dal for dal in inputs.dal_list if dal['abrev'] == 'LinK'] ### {abrev, path, pattern}
    
    dal_ref    = [{'LinK':dal['pattern']} for dal in ref] ## [{'LinK':pattern}]
    path_to_ref = ref[0]['path_to_files']

    dals = [dal for dal in inputs.dal_list if dal['abrev'] != 'LinK'] ## [{abrev, path, pattern}, {abrev, path, pattern}, ...]
    list_func = get_list_functionals(dals)

    list_ADMM = get_list_ADMM(dals)

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
                    ## single gradient (LinK) calculation, without ADMM
                    ## ex.: ls lsd*Histidine*out | grep -v ADMM
                    cmd= "ls "+ path_to_ref+"/lsd*"+dal_ref[0]['LinK']+"*"+regBasis+"*"+mol+"*.out  | grep -v ADMM[2,S]"
                    file_ref = run_command_or_exit(cmd)
                    # if file_ref != None:
                    #     print "\t\t"+file_ref
                    
                    cmd= "ls "+ path_to_dals+"/lsd*"+dalPattern+"*"+regBasis+"*"+mol+"*.out"
                    files_dal = run_command_or_exit(cmd)
                    if files_dal != None and len((files_dal.strip()).split("\n")) != 1:
                        file_dal = files_dal[0].strip()
                        print "CAREFUL: this 'ls' command returns more than one file:\n",cmd
                        raw_input("Press Enter to continue...")
                    else:
                        file_dal = files_dal
                    # if file_dal != None:
                    #     print "\t\t"+file_dal

                    
                    ## compare gradient of reference with ADMM
                    #print file_ref
                    diffGrad = compLS.get_compareInfoGradients(file_ref, file_dal)
                    #diffGrad = compLS.get_compareInfoGradients(file_dal)
                    #print diffGrad
                    if diffGrad != None:
                        ## make sure that reference and ADMM calculation have matching geometries
                        ## here the LinK reference (geom.opt) converged geometry is the input for 
                        ## the ADMM single gradient calculations, so ...
                        error_message = 'Nuclear repulsion contribution not matching, check you are comparing same initial/converged geometries:\r' + file_ref + "\rfile_dal:\r" + file_dal
                        npt.assert_approx_equal(readLS.get_energy_contribution_lastNuclearRepulsion(file_ref), readLS.get_energy_contribution_firstNuclearRepulsion(file_dal), significant=9,
                                                err_msg=error_message, verbose=True)
                        results[regBasis][func][admm][mol] =  stats.matrix( diffGrad['matDiffGrad'] ).get_stats()
                    else:
                        combinationAvoided.append([regBasis, func, admm, mol])
    avoidedCases = "\n".join(["\t".join(combi) for combi in combinationAvoided])
    if avoidedCases != "":
        print "Combinations avoided:"
        print avoidedCases
    return results


def generate_table(inputs, results, path_to_file):
    basis_list = [bas['pattern'] for bas in inputs.basisSets]  ### 6-31Gs   
    mol_list   = inputs.mol_list ## [molecule_name]
    dals = [dal for dal in inputs.dal_list if dal['abrev'] != 'LinK'] ## [{abrev, path, pattern}, {abrev, path, pattern}, ...]
    list_func = get_list_functionals(dals)
    list_ADMM = get_list_ADMM(dals)

    csvRows = []

    for molVal  in mol_list:
        columnHeaders = ['Molecule']
        mol  = molVal.strip()
        #print mol
        newRow = {}
        newRow['Molecule'] = mol
        for regBasisVal in basis_list:
            regBasis = regBasisVal.strip()  
            #print "\t"+regBasis
            for typeADMM in list_ADMM:
                #print "\t\t\t"+ typeADMM
                for typeFunc in list_func:
                    #print "\t\t" + typeFunc
                    header = "\r" + regBasis + "\r" + typeADMM + "(3-21G)\r" + typeFunc
                    headerMean     = "Mean" + header
                    headerStdDev   = "StdDev" + header
                    headerVariance = "Var" + header
                    headerMaxAbs   = "Max.Abs. (mEh)" + header
                    headerRMS      = "RMS (mEh)" + header
                    #columnHeaders.append(headerMean.strip())
                    #columnHeaders.append(headerStdDev.strip())
                    #columnHeaders.append(headerVariance.strip())
                    columnHeaders.append(headerRMS.strip())
                    #columnHeaders.append(headerMaxAbs.strip())
                    if results[regBasis][typeFunc][typeADMM][mol] != {}:
                        #newRow[headerMean.strip()]     = results[regBasis][typeFunc][typeADMM][mol]['mean']
                        #newRow[headerStdDev.strip()]   = results[regBasis][typeFunc][typeADMM][mol]['stdDev']
                        #newRow[headerVariance.strip()] = results[regBasis][typeFunc][typeADMM][mol]['variance']
                        newRow[headerRMS.strip()]      = results[regBasis][typeFunc][typeADMM][mol]['rms']*1000.
                        #newRow[headerMaxAbs.strip()]   = results[regBasis][typeFunc][typeADMM][mol]['maxAbs']
            for typeADMM in list_ADMM:
                #print "\t\t\t"+ typeADMM
                for typeFunc in list_func:
                    #print "\t\t" + typeFunc
                    header = "\r" + regBasis + "\r" + typeADMM + "(3-21G)\r" + typeFunc
                    headerMean     = "Mean" + header
                    headerStdDev   = "StdDev" + header
                    headerVariance = "Var" + header
                    headerMaxAbs   = "Max.Abs. (mEh)" + header
                    headerRMS      = "RMS (mEh)" + header
                    #columnHeaders.append(headerMean.strip())
                    #columnHeaders.append(headerStdDev.strip())
                    #columnHeaders.append(headerVariance.strip())
                    #columnHeaders.append(headerRMS.strip())
                    columnHeaders.append(headerMaxAbs.strip())
                    if results[regBasis][typeFunc][typeADMM][mol] != {}:
                        #newRow[headerMean.strip()]     = results[regBasis][typeFunc][typeADMM][mol]['mean']
                        #newRow[headerStdDev.strip()]   = results[regBasis][typeFunc][typeADMM][mol]['stdDev']
                        #newRow[headerVariance.strip()] = results[regBasis][typeFunc][typeADMM][mol]['variance']
                        #newRow[headerRMS.strip()]      = results[regBasis][typeFunc][typeADMM][mol]['rms']
                        newRow[headerMaxAbs.strip()]   = results[regBasis][typeFunc][typeADMM][mol]['maxAbs']*1000.
        #print newRow
        csvRows.append(newRow)
    with open(path_to_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columnHeaders)
        writer.writeheader()
        [writer.writerow(row) for row in csvRows]
    print "Output csv table generated here: ", path_to_file

if __name__ == "__main__":
    run()
