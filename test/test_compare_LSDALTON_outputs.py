#!/usr/bin/env python

import unittest
import read_LSDALTON_output as readLS
import compare_LSDALTON_outputs as compareLS
import numpy as np

# http://docs.python-guide.org/en/latest/writing/tests/
# http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure


class compare_molecular_gradients(unittest.TestCase):

    def setUp(self):
        self.path_to_file1 = "../files/lsdalton_files/lsdalton20140924_geomOpt-b3lyp_Vanlenthe_6-31G_df-def2_Histidine_2CPU_16OMP_2014_10_28T1007.out"
        self.path_to_file2 = "../files/lsdalton_files/lsdalton20140924_b3lyp_gradient_ADMM2_6-31Gs_df-def2_3-21G_Histidine_8CPU_16OMP_2014_11_17T1502.out"
        self.zeroDiff = compareLS.get_compareInfoGradients(self.path_to_file1, self.path_to_file1)
        self.diffGrad = compareLS.get_compareInfoGradients(self.path_to_file1, self.path_to_file2)
		
    def test_compare_same_gradient_infos_from_two_files(self):
        [self.assertEqual(self.zeroDiff[key], 0.) for key in ['maxDiffGrad','minDiffGrad','rmsDiffGrad']] 


    def test_compare_different_gradients_infos_from_two_files(self):
        stored_diffGrad = {'maxDiffGrad': 0.0027560541,
                           'rmsDiffGrad': 0.0007914322208658989,
                           'minDiffGrad': 9.4533000000000032e-06}
        [self.assertEqual(self.diffGrad[key], stored_diffGrad[key]) for key in ['maxDiffGrad','minDiffGrad','rmsDiffGrad']] 

    def test_compare_matrix_difference_btw_two_gradients(self):
        diffGrad_stored = np.array([[4.22896e-05, -0.0001704826, 0.0003147501], [6.47043e-05, 7.4662e-05, 0.0006172063], [2.30515e-05, -0.000309106, 0.000219824], [-0.0002165726, -0.0002996764, 0.0002543384], [5.33383e-05, 0.0001018354, 0.0002260922], [-0.0001310191, 0.0001602674, -0.0001566449], [-6.10757e-05, 0.0002359704, -0.0003841592], [-0.0002007452, -0.0002688735, 0.0003078568], [0.0001835822, -1.80844e-05, 0.0003050426], [0.00202674, 0.0013095427, 0.0007275789], [-0.0005020716, -0.0013372284, 0.0014625098], [0.0010077123, 0.0014691394, -0.0015769903], [-0.0002942884, 2.06135e-05, -0.001155602], [0.0008384236, -0.000432685, -0.0003130658], [-0.0004334554, 0.0001199964, 0.0009870985], [0.0001248103, 0.0008244539, 0.0002500715], [2.08764e-05, -8.97295e-05, 0.0001601153], [-0.0008798945, -0.0001947693, -0.0009349563], [-0.0016785601, -0.0011252948, -0.0027560541], [9.4533e-06, -6.28408e-05, 0.001449541]])
        [self.assertAlmostEqual(elem[0],elem[1], places=9) for elem in zip(self.diffGrad['matDiffGrad'].flatten(),diffGrad_stored.flatten())]
        

if __name__ == '__main__':
    unittest.main()
