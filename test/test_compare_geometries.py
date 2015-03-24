#!/usr/bin/env python

import unittest
import numpy as np
#import read_LSDALTON_output as readLS
import compare_geometries as compGeo



class compare_RMS_Deviation(unittest.TestCase):

    def setUp(self):
        self.path_to_file1 = "../src/files/Histidine_input.xyz"
        self.path_to_file2 = "../src/files/Histidine_optimized.xyz"
        self.zeroDiff = compGeo.get_RMS_deviation(self.path_to_file1, self.path_to_file1)
        self.diffGeom = compGeo.get_RMS_deviation(self.path_to_file1, self.path_to_file2)
		
    def test_compare_same_geometries(self):
        [self.assertAlmostEqual(self.zeroDiff[key], 0., places=12) for key in self.zeroDiff.keys()] 


    def test_compare_Input_vs_optimized_geoemtries_of_Histidine(self):
        stored_RMSD = {'Fitted RMSD': 0.0035478001322117462,
                       'Normal RMSD': 0.0035478001464218515,
                       'Kabsch RMSD': 0.0035478001322117462}
        [self.assertAlmostEqual(stored_RMSD[key],self.diffGeom[key], places=12) for key in stored_RMSD.keys()]

if __name__ == '__main__':
    unittest.main()
