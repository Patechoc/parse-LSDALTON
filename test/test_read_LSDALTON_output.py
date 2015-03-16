#!/usr/bin/env python 

import unittest
import random
import read_LSDALTON_output as readLS
import numpy as np

# http://docs.python-guide.org/en/latest/writing/tests/
# http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure

class demo_test(unittest.TestCase):

    def setUp(self):
        self.seq = list(range(10))

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, list(range(10)))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

class read_molecule_input_from_output(unittest.TestCase):
    def setUp(self):
        self.path_to_file1 = "../src/files/lsdalton_files/lsdalton20140924_geomOpt-b3lyp_Vanlenthe_6-31G_df-def2_Histidine_2CPU_16OMP_2014_10_28T1007.out"
        self.moleculeString1 = """  BASIS                                   
        6-31G Aux=df-def2 ADMM=3-21G            
        geometry optimized with ADMM2 using 6-31
        Output is in Bohr                       
        Atomtypes=4    Charge=0   Nosymmetry                        
        Charge=1.00   Atoms=9                                       
        H         -2.17356347      1.90522337      0.25455721       
        H         -3.75123607     -0.45217796      5.47452789       
        H         -2.01838203      3.45689709      4.42293912       
        H          0.57566832      1.67201802      4.68768673       
        H         -0.23802027     -2.23988209     -0.80154881       
        H          0.63072116     -2.70463484      2.37334503       
        H          5.35514085     -0.69790796      3.77725447       
        H          6.58755095      3.88494216     -2.59138922       
        H          2.17043033      1.91921391     -3.03488365       
        Charge=6.00   Atoms=6                                       
        C         -4.24934301     -1.10402006      1.98975136       
        C          4.96884265      0.25477395      2.01772251       
        C          5.72157696      2.63568946     -1.23773826       
        C         -1.83317562      0.50674782      1.74863024       
        C          0.37525319     -1.25493030      0.91450618       
        C          2.82257191      0.09684848      0.53706767       
        Charge=7.00   Atoms=3                                       
        N         -1.28625882      1.69450024      4.21200748       
        N          6.76332980      1.83602818      0.90136254       
        N          3.32602362      1.64162689     -1.54496487       
        Charge=8.00   Atoms=2                                       
        O         -5.33156510     -2.03936977      0.15402194       
        O         -4.99044067     -1.45108413      4.42837147"""

    def test_extracting_moleculeString_from_output(self):
        str_mol1 = readLS.get_input_MOL_string(self.path_to_file1)
        stripped_molstr = "\n".join([line.strip() for line in self.moleculeString1.split('\n')])
        self.assertEqual(str_mol1.strip(), stripped_molstr.strip())        
    def test_parsing_moleculeString(self):
        str_mol1 = readLS.get_input_MOL_string(self.path_to_file1)
        parsedInfo = readLS.parse_MOL_string(str_mol1)


class energy_contributions(unittest.TestCase):
    def setUp(self):
        self.path_to_file = "../src/files/lsdalton_files/lsdalton20140924_geomOpt-b3lyp_Vanlenthe_6-31G_df-def2_Histidine_2CPU_16OMP_2014_10_28T1007.out"
        self.list_nucRep = [601.971967502122, 601.979053253774, 601.992494863707, 601.986070908488, 602.029206129620, 602.000169297309]
        self.nuclear_repulsions = readLS.get_energy_contribution_nuclearRepulsion(self.path_to_file)
    def test_nuclearRepulsion_geomOpt(self):
        [self.assertEqual(float(elems[0]), elems[1]) for elems in zip(self.nuclear_repulsions, self.list_nucRep)]
    def test_firstNuclearRepulsion(self):
        self.assertEqual(self.list_nucRep[0], readLS.get_energy_contribution_firstNuclearRepulsion(self.path_to_file)) 
    def test_lastNuclearRepulsion(self):
        self.assertEqual(self.list_nucRep[-1], readLS.get_energy_contribution_lastNuclearRepulsion(self.path_to_file)) 


class molecular_gradient(unittest.TestCase):
    def setUp(self):
        self.path_to_file = "../src/files/lsdalton_files/lsdalton20140924_geomOpt-b3lyp_Vanlenthe_6-31G_df-def2_Histidine_2CPU_16OMP_2014_10_28T1007.out"
        self.grad = readLS.get_last_molecular_gradient(self.path_to_file)
		
    def test_extract_gradient_to_file(self):
        grad_01 = [{'y': '0.0000014502', 'x': '-0.0000106785', 'z': '-0.0000085260', 'atom': 'H'},
                   {'y': '0.0000563897', 'x': '0.0000638938', 'z': '0.0000176832', 'atom': 'H'},
                   {'y': '0.0000086022', 'x': '0.0000044989', 'z': '-0.0000023849', 'atom': 'H'},
                   {'y': '0.0000095950', 'x': '0.0000119114', 'z': '0.0000044454', 'atom': 'H'},
                   {'y': '-0.0000103279', 'x': '-0.0000056952', 'z': '-0.0000116304', 'atom': 'H'},
                   {'y': '-0.0000096328', 'x': '0.0000104919', 'z': '0.0000057410', 'atom': 'H'},
                   {'y': '-0.0000088125', 'x': '0.0000083083', 'z': '0.0000119956', 'atom': 'H'},
                   {'y': '0.0000152898', 'x': '0.0000037704', 'z': '-0.0000087830', 'atom': 'H'},
                   {'y': '-0.0000103254', 'x': '0.0000098959', 'z': '0.0000028204', 'atom': 'H'},
                   {'y': '0.0000028250', 'x': '-0.0000732077', 'z': '0.0000780527', 'atom': 'C'},
                   {'y': '0.0000063098', 'x': '0.0000353762', 'z': '0.0000072911', 'atom': 'C'},
                   {'y': '-0.0000122764', 'x': '-0.0000439422', 'z': '0.0000111221', 'atom': 'C'},
                   {'y': '-0.0000364624', 'x': '0.0000406470', 'z': '0.0000024698', 'atom': 'C'},
                   {'y': '0.0000292506', 'x': '-0.0000706660', 'z': '0.0000217727', 'atom': 'C'},
                   {'y': '0.0000447619', 'x': '-0.0000142704', 'z': '-0.0000480324', 'atom': 'C'},
                   {'y': '-0.0000339819', 'x': '-0.0000259069', 'z': '0.0000053035', 'atom': 'N'},
                   {'y': '-0.0000144038', 'x': '-0.0000045786', 'z': '0.0000047574', 'atom': 'N'},
                   {'y': '-0.0000090433', 'x': '0.0000407596', 'z': '0.0000124914', 'atom': 'N'},
                   {'y': '0.0000049723', 'x': '0.0000363805', 'z': '-0.0000290822', 'atom': 'O'},
                   {'y': '-0.0000333703', 'x': '-0.0000222115', 'z': '-0.0000752538', 'atom': 'O'}]
        [ [self.assertEqual(elems[0][key], elems[1][key]) for key in ['atom','x','y','z']] for elems in zip(self.grad,grad_01)  ]

    def test_get_infoGradient_from_gradString(self):
        obj = readLS.get_infoGradient_from_gradString(self.grad)
        obj_stored = {'minGrad': 1.4501999999999999e-06, 'maxGrad': 7.8052699999999999e-05, 'rmsGrad': 2.937091073023046e-05}
        [self.assertEqual(obj[key], obj_stored[key]) for key in ['minGrad','maxGrad','rmsGrad']]
        grad_stored = [['H', np.array([ -1.06785000e-05,   1.45020000e-06,  -8.52600000e-06])],
                       ['H', np.array([  6.38938000e-05,   5.63897000e-05,   1.76832000e-05])],
                       ['H', np.array([  4.49890000e-06,   8.60220000e-06,  -2.38490000e-06])],
                       ['H', np.array([  1.19114000e-05,   9.59500000e-06,   4.44540000e-06])],
                       ['H', np.array([ -5.69520000e-06,  -1.03279000e-05,  -1.16304000e-05])],
                       ['H', np.array([  1.04919000e-05,  -9.63280000e-06,   5.74100000e-06])],
                       ['H', np.array([  8.30830000e-06,  -8.81250000e-06,   1.19956000e-05])],
                       ['H', np.array([  3.77040000e-06,   1.52898000e-05,  -8.78300000e-06])],
                       ['H', np.array([  9.89590000e-06,  -1.03254000e-05,   2.82040000e-06])],
                       ['C', np.array([ -7.32077000e-05,   2.82500000e-06,   7.80527000e-05])],
                       ['C', np.array([  3.53762000e-05,   6.30980000e-06,   7.29110000e-06])],
                       ['C', np.array([ -4.39422000e-05,  -1.22764000e-05,   1.11221000e-05])],
                       ['C', np.array([  4.06470000e-05,  -3.64624000e-05,   2.46980000e-06])],
                       ['C', np.array([ -7.06660000e-05,   2.92506000e-05,   2.17727000e-05])],
                       ['C', np.array([ -1.42704000e-05,   4.47619000e-05,  -4.80324000e-05])],
                       ['N', np.array([ -2.59069000e-05,  -3.39819000e-05,   5.30350000e-06])],
                       ['N', np.array([ -4.57860000e-06,  -1.44038000e-05,   4.75740000e-06])],
                       ['N', np.array([  4.07596000e-05,  -9.04330000e-06,   1.24914000e-05])],
                       ['O', np.array([  3.63805000e-05,   4.97230000e-06,  -2.90822000e-05])],
                       ['O', np.array([ -2.22115000e-05,  -3.33703000e-05,  -7.52538000e-05])]]
        [self.assertEqual(elem[0][0],elem[1][0]) for elem in zip(obj['gradient'],grad_stored)]
        [self.assertTrue(np.array_equal(elem[0][1],elem[1][1])) for elem in zip(obj['gradient'],grad_stored)]
        



if __name__ == '__main__':
    unittest.main()
