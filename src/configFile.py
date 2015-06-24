#!/usr/bin/env python
import sys
import molecule_sets
from datetime import date


today = date.today()
today_str = today.isoformat()


class InputAnalysis(object):
    def __init__(self, title=today_str):
        self.title = title
        self.mol_list = []
        self.dal_list = []
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

    def __str__(self):
        str = "Title:\n{}".format(self.title)
        str += "\n\tMolecules:\n\t\t- "+ "\n\t\t- ".join(self.mol_list)
        str += "\n\tDalton inputs:\n\t\t- "+ "\n\t\t- ".join(dal['abrev'] for dal in self.dal_list)
        str += "\n\tBasis sets:\n\t\t- "+ "\n\t\t- ".join(basis['abrev']+" ("+basis['type']+")" for basis in self.basisSets)
        return str


def get_inputs(title):
    inputs = InputAnalysis(title)
    if (title == "ADMM2/ADMMS (6-31G*/3-21G) single gradient deviation from geom. opt. ref. (6-31G*)"):
        mol_list = ['Histidine','Ferrocene']
        #mol_list = [mol.shortname for mol in molecule_sets.get_moleculeSet_benchmark_geomOpt()]
        path_to_ref = '/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_6-31Gs/'
        dal_list = [{'abrev':'LinK', 'pattern':'geomOpt-b3lyp_Vanlenthe', 'path_to_files':path_to_ref }]

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


    elif (title == "ADMM single SCF + gradient error from LinK reference (6-31G*/3-21G)"):
        print "Title found: ",title
        #mol_list = ['Histidine','Ferrocene']
        mol_list = [mol.shortname for mol in molecule_sets.get_moleculeSet_benchmark_geomOpt()]
        path_to_ref = '/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_6-31Gs/'

        #dal_list = [{'abrev':'LinK', 'pattern':'b3lyp_gradient_', 'path_to_files':path_to_ref }]  ### single gradient LinK calc.
        dal_list = [{'abrev':'LinK', 'pattern':'geomOpt-b3lyp_Vanlenthe', 'path_to_files':path_to_ref }]  ### geometry optimized LinK calc.

        path_to_dals = path_to_ref
        dals = [{'abrev':'ADMM2-KT3X', 'pattern':'b3lyp_gradient_ADMM2-KT3X_', 'path_to_files':path_to_ref},
                {'abrev':'ADMM2-OPTX', 'pattern':'b3lyp_gradient_ADMM2-OPTX_', 'path_to_files':path_to_ref},
                {'abrev':'ADMM2-B88X', 'pattern':'b3lyp_gradient_ADMM2_',      'path_to_files':path_to_ref},
                {'abrev':'ADMM2-PBEX', 'pattern':'b3lyp_gradient_ADMM2-PBEX_', 'path_to_files':path_to_ref},
                {'abrev':'ADMMS-KT3X', 'pattern':'b3lyp_gradient_ADMMS-KT3X_', 'path_to_files':path_to_ref},
                {'abrev':'ADMMS-OPTX', 'pattern':'b3lyp_gradient_ADMMS-OPTX_', 'path_to_files':path_to_ref},
                {'abrev':'ADMMS-B88X', 'pattern':'b3lyp_gradient_ADMMS-B86X_', 'path_to_files':path_to_ref},
                {'abrev':'ADMMS-PBEX', 'pattern':'b3lyp_gradient_ADMMS-PBEX_', 'path_to_files':path_to_ref}]
        dal_list.extend(dals)
        basisSets = [{'type':'regBasis', 'abrev':'6-31G*','pattern':'6-31Gs'}]
        doPlot = True
        inputs.set_inputs(title, mol_list, dal_list, basisSets, doPlot)    


    elif (title == "ADMM single SCF + gradient error from LinK reference (cc-pVTZ/3-21G)"):
        print "Title found: ",title
        #mol_list = ['Histidine','Ferrocene']
        mol_list = [mol.shortname for mol in molecule_sets.get_moleculeSet_benchmark_geomOpt()]
        path_to_ref = '/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_cc-pVTZ/'
        #dal_list = [{'abrev':'LinK', 'pattern':'b3lyp_gradient_', 'path_to_files':path_to_ref }]  ### single gradient LinK calc.
        dal_list = [{'abrev':'LinK', 'pattern':'geomOpt-b3lyp_Vanlenthe', 'path_to_files':path_to_ref }]  ### geometry optimized LinK calc.

        path_to_dals = path_to_ref
        dals = [{'abrev':'ADMM2-KT3X', 'pattern':'b3lyp_gradient_ADMM2-KT3X_', 'path_to_files':path_to_dals},
                {'abrev':'ADMM2-OPTX', 'pattern':'b3lyp_gradient_ADMM2-OPTX_', 'path_to_files':path_to_dals},
                {'abrev':'ADMM2-B88X', 'pattern':'b3lyp_gradient_ADMM2-B8',      'path_to_files':path_to_dals},
                {'abrev':'ADMM2-PBEX', 'pattern':'b3lyp_gradient_ADMM2-PBEX_', 'path_to_files':path_to_dals},
                {'abrev':'ADMMS-KT3X', 'pattern':'b3lyp_gradient_ADMMS-KT3X_', 'path_to_files':path_to_dals},
                {'abrev':'ADMMS-OPTX', 'pattern':'b3lyp_gradient_ADMMS-OPTX_', 'path_to_files':path_to_dals},
                {'abrev':'ADMMS-B88X', 'pattern':'b3lyp_gradient_ADMMS-B8', 'path_to_files':path_to_dals},
                {'abrev':'ADMMS-PBEX', 'pattern':'b3lyp_gradient_ADMMS-PBEX_', 'path_to_files':path_to_dals}]
        dal_list.extend(dals)
        basisSets = [{'type':'regBasis', 'abrev':'cc-pVTZ','pattern':'cc-pVTZ'}]
        doPlot = True
        inputs.set_inputs(title, mol_list, dal_list, basisSets, doPlot)    



    elif (title == "RMS deviation between optimized geometries (LinK/6-31G* vs LinK/cc-pVTZ)"):
        print "Title found: ",title
        #mol_list = ['Histidine','Ferrocene']
        #mol_list = [mol.shortname for mol in molecule_sets.get_moleculeSet_benchmark_geomOpt()]
        mol_list = ['taxol','valinomycin']
        path_to_ref = '/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_cc-pVTZ'
        dal_list = [{'abrev':'LinK/cc-pVTZ', 'pattern':'geomOpt-b3lyp_Vanlenthe_cc-pVTZ', 'path_to_files':path_to_ref }]  ### geometry optimized LinK calc.

        path_to_dals = '/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_6-31Gs'
        dals = [{'abrev':'LinK/6-31G*', 'pattern':'geomOpt-b3lyp_Vanlenthe_6-31Gs', 'path_to_files':path_to_dals}]
        dal_list.extend(dals)
        basisSets = [{'type':'regBasis', 'abrev':'cc-pVTZ','pattern':'cc-pVTZ'},
                     {'type':'regBasis', 'abrev':'6-31G*','pattern':'6-31Gs'}]
        doPlot = False
        inputs.set_inputs(title, mol_list, dal_list, basisSets, doPlot)

    elif (title == "RMS deviation of ADMM optimized geometries (compared to LinK/6-31G* and LinK/cc-pVTZ optimized geometries)"):
        print "Title found: ",title
        #mol_list = ['Histidine','Ferrocene']
        #mol_list = [mol.shortname for mol in molecule_sets.get_moleculeSet_benchmark_geomOpt()]
        mol_list = ['taxol','valinomycin']
        path_to_ref = ['/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_cc-pVTZ',
                       '/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_6-31Gs']
        dal_list = [{'abrev':'LinK', 'pattern':'geomOpt-b3lyp_Vanlenthe', 'path_to_files':path_to_ref }]  ### geometry optimized LinK calc.

        path_to_dals = '/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/ADMM_geometry_optimization'
        dals = [{'abrev':'ADMM2-KT3X', 'pattern':'geomOpt-b3lyp_ADMM2-KT3X', 'path_to_files':path_to_dals},
                {'abrev':'ADMM2-OPTX', 'pattern':'geomOpt-b3lyp_ADMM2-OPTX', 'path_to_files':path_to_dals},
                {'abrev':'ADMM2-B88X', 'pattern':'geomOpt-b3lyp_ADMM2-B8',      'path_to_files':path_to_dals},
                {'abrev':'ADMM2-PBEX', 'pattern':'geomOpt-b3lyp_ADMM2-PBEX', 'path_to_files':path_to_dals},
                {'abrev':'ADMMS-KT3X', 'pattern':'geomOpt-b3lyp_ADMMS-KT3X', 'path_to_files':path_to_dals},
                {'abrev':'ADMMS-OPTX', 'pattern':'geomOpt-b3lyp_ADMMS-OPTX', 'path_to_files':path_to_dals},
                {'abrev':'ADMMS-B88X', 'pattern':'geomOpt-b3lyp_ADMMS-B8', 'path_to_files':path_to_dals},
                {'abrev':'ADMMS-PBEX', 'pattern':'geomOpt-b3lyp_ADMMS-PBEX', 'path_to_files':path_to_dals}]
        dal_list.extend(dals)
        basisSets = [{'type':'regBasis', 'abrev':'cc-pVTZ','pattern':'cc-pVTZ'},
                     {'type':'regBasis', 'abrev':'6-31G*','pattern':'6-31Gs'}]
        doPlot = False
        inputs.set_inputs(title, mol_list, dal_list, basisSets, doPlot)

    elif (title == "Test of Topology differences between optimized geometries of Valinomycin (cc-pVTZ)"):
        print "Title found: ",title
        mol_list = ['valinomycin'] #['taxol','valinomycin']
        path_to_ref = "/home/ctcc2/Documents/CODE-DEV/xyz2top/xyz2top/tests/files/"
        dal_list = [{'abrev':'LinK', 'pattern':'geomOpt_DFT-b3lyp', 'path_to_files':path_to_ref }]

        path_to_dals = path_to_ref
        dals = [{'abrev':'LinK-noDF', 'pattern':'geomOpt_DFT-b3lyp-noDF', 'path_to_files':path_to_dals}]
        dal_list.extend(dals)
        basisSets = [{'type':'regBasis', 'abrev':'cc-pVTZ','pattern':'cc-pVTZ'}]#,
                     #{'type':'regBasis', 'abrev':'6-31G*','pattern':'6-31Gs'}]
        doPlot = True
        inputs.set_inputs(title, mol_list, dal_list, basisSets, doPlot)

    elif (title == "Topology deviations due to density-fitting"):
        print "Title found: ",title
        mol_list = ['c180','valinomycin'] #['taxol','valinomycin']
        path_cc_pVTZ = "/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_cc-pVTZ"
        path_6_31Gs = "/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_6-31Gs"
        dal_list = [{'abrev':'LinK-noDF',
                     'pattern':'geomOpt-b3lyp_Vanlenthe_noDF',
                     'path_to_files':[path_cc_pVTZ, path_6_31Gs] },
                    {'abrev':'LinK',
                     'pattern':'geomOpt-b3lyp_Vanlenthe',
                     'path_to_files':[path_cc_pVTZ, path_6_31Gs] }]


        basisSets = [{'type':'regBasis', 'abrev':'cc-pVTZ','pattern':'cc-pVTZ'},
                     {'type':'auxBasis', 'abrev':'df-def2','pattern':'df-def2'},
                     {'type':'auxBasis', 'abrev':'cc-pVTZdenfit','pattern':'cc-pVTZdenfit'},
                     {'type':'regBasis', 'abrev':'6-31G*','pattern':'6-31Gs'}]
        doPlot = True
        inputs.set_inputs(title, mol_list, dal_list, basisSets, doPlot)

    elif (title == "Topology deviations due to basis set error"):
        print "Title found: ",title
        mol_list = ['c180','valinomycin'] #['taxol','valinomycin']
        path_cc_pVTZ = "/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_cc-pVTZ"
        path_6_31Gs = "/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_6-31Gs"
        dal_list = [{'abrev':'LinK-noDF',
                     'pattern':'geomOpt-b3lyp_Vanlenthe_noDF',
                     'path_to_files':[path_cc_pVTZ, path_6_31Gs] },
                    {'abrev':'LinK',
                     'pattern':'geomOpt-b3lyp_Vanlenthe',
                     'path_to_files':[path_cc_pVTZ, path_6_31Gs] }]


        basisSets = [{'type':'regBasis', 'abrev':'cc-pVTZ','pattern':'cc-pVTZ'},
                     {'type':'auxBasis', 'abrev':'df-def2','pattern':'df-def2'},
                     {'type':'auxBasis', 'abrev':'cc-pVTZdenfit','pattern':'cc-pVTZdenfit'},
                     {'type':'regBasis', 'abrev':'6-31G*','pattern':'6-31Gs'}]
        doPlot = True
        inputs.set_inputs(title, mol_list, dal_list, basisSets, doPlot)


    else:
        print "Title for the configuration setup not recognized!!!!"
        sys.exit()
    return inputs
