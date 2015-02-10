#!/usr/bin/env python
import molecules
from datetime import date


today = date.today()
today_str = today.isoformat()


#mol_list = ['Histidine','Ferrocene']
mol_list = [mol.shortname for mol in molecules.get_moleculeSet_benchmark_geomOpt()]

basis_list = ['6-31Gs']

dal_ref = [{'LinK':'geomOpt-b3lyp_Vanlenthe_'}]
path_to_ref = "/home/ctcc2/Documents/LSDALTON/SIMULATIONS/RESULTS_ADMM_geomOpt/benchmark_6-31Gs"

dal_list = [{'abrev':'ADMM2-OPTX', 'pattern':'b3lyp_gradient_ADMM2-OPTX_'},
            {'abrev':'ADMM2-KT3X', 'pattern':'b3lyp_gradient_ADMM2-KT3X_'},
            {'abrev':'ADMM2-B88X', 'pattern':'b3lyp_gradient_ADMM2_'},
            {'abrev':'ADMMS-OPTX', 'pattern':'b3lyp_gradient_ADMMS-OPTX_'},
            {'abrev':'ADMMS-KT3X', 'pattern':'b3lyp_gradient_ADMMS-KT3X_'},
            {'abrev':'ADMMS-B88X', 'pattern':'b3lyp_gradient_ADMMS-B86X_'}]
path_to_dals = path_to_ref



title =  'ADMM2/ADMMS (6-31G*/3-21G) single gradient deviation from geom. opt. ref. (6-31G*)'
