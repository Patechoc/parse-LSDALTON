#!/usr/bin/env python
import molecules
from datetime import date


today = date.today()
today_str = today.isoformat()


class InputAnalysis(object):
    def __init__(self, title=today_str):
        self.title = title
        self.mol_list = []
        self.dal_ref  = []
        self.doPlot = False
        self.basisSets = []

    def set_inputs(self, title, mol_list=[], dal_list=[], basisSets=[], doPlot=False):
        self.title = title
        self.mol_list = mol_list
        self.dal_list = dal_list
        self.basisSets = basisSets
        self.doPlot = doPlot
        return self

def get_inputs(title):
    inputs = InputAnalysis(title)
    if (title == "ADMM2/ADMMS (6-31G*/3-21G) single gradient deviation from geom. opt. ref. (6-31G*)"):
        #mol_list = ['Histidine','Ferrocene']
        mol_list = [mol.shortname for mol in molecules.get_moleculeSet_benchmark_geomOpt()]
        path_to_ref = '/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_6-31Gs/'
        dal_list = [{'abrev':'LinK', 'pattern':'geomOpt-b3lyp_Vanlenthe_', 'path_to_files':path_to_ref }]

        path_to_dals = path_to_ref
        dals = [{'abrev':'ADMM2-OPTX', 'pattern':'b3lyp_gradient_ADMM2-OPTX_', 'path_to_files':path_to_ref},
                {'abrev':'ADMM2-KT3X', 'pattern':'b3lyp_gradient_ADMM2-KT3X_', 'path_to_files':path_to_ref},
                {'abrev':'ADMM2-B88X', 'pattern':'b3lyp_gradient_ADMM2_',      'path_to_files':path_to_ref},
                {'abrev':'ADMMS-OPTX', 'pattern':'b3lyp_gradient_ADMMS-OPTX_', 'path_to_files':path_to_ref},
                {'abrev':'ADMMS-KT3X', 'pattern':'b3lyp_gradient_ADMMS-KT3X_', 'path_to_files':path_to_ref},
                {'abrev':'ADMMS-B88X', 'pattern':'b3lyp_gradient_ADMMS-B86X_', 'path_to_files':path_to_ref}]
        dal_list.extend(dals)
        basisSets = [{'type':'regBasis', 'abrev':'6-31G*','pattern':'6-31Gs'}]
        doPlot = False
        inputs.set_inputs(title, mol_list, dal_list, basisSets, doPlot)
    elif (title == "ADMM single SCF + gradient error from LinK reference (6-31G*/3-21G and cc-pVTZ/3-21G)"):
        mol_list = ['Histidine','Ferrocene']
        #mol_list = [mol.shortname for mol in molecules.get_moleculeSet_benchmark_geomOpt()]
        path_to_ref = '/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_6-31Gs/'
        dal_list = [{'abrev':'LinK', 'pattern':'geomOpt-b3lyp_Vanlenthe_', 'path_to_files':path_to_ref }]

        path_to_dals = path_to_ref
        dals = [{'abrev':'ADMM2-OPTX', 'pattern':'b3lyp_gradient_ADMM2-OPTX_', 'path_to_files':path_to_ref},
                {'abrev':'ADMM2-KT3X', 'pattern':'b3lyp_gradient_ADMM2-KT3X_', 'path_to_files':path_to_ref},
                {'abrev':'ADMM2-B88X', 'pattern':'b3lyp_gradient_ADMM2_',      'path_to_files':path_to_ref},
                {'abrev':'ADMMS-OPTX', 'pattern':'b3lyp_gradient_ADMMS-OPTX_', 'path_to_files':path_to_ref},
                {'abrev':'ADMMS-KT3X', 'pattern':'b3lyp_gradient_ADMMS-KT3X_', 'path_to_files':path_to_ref},
                {'abrev':'ADMMS-B88X', 'pattern':'b3lyp_gradient_ADMMS-B86X_', 'path_to_files':path_to_ref}]
        dal_list.extend(dals)
        basisSets = [{'type':'regBasis', 'abrev':'6-31G*','pattern':'6-31Gs'}]
        doPlot = True
        inputs.set_inputs(title, mol_list, dal_list, basisSets, doPlot)    
    return inputs