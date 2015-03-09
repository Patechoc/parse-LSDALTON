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


class molecular_gradient(unittest.TestCase):

    def setUp(self):
        self.path_to_file = "../files/lsdalton_files/lsdalton20140924_geomOpt-b3lyp_Vanlenthe_6-31G_df-def2_Histidine_2CPU_16OMP_2014_10_28T1007.out"
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
