#!/usr/bin/env python 

import unittest
import numpy as np
import statistics as stats

# http://docs.python-guide.org/en/latest/writing/tests/
# http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure

class matrix_statistics(unittest.TestCase):

    def setUp(self):
        self.matrix01 = np.array([[1, 2], [3, 4]])
        self.matrix02 = np.array([[ -1.06785000e-05,   1.45020000e-06,  -8.52600000e-06],
                                  [  6.38938000e-05,   5.63897000e-05,   1.76832000e-05],
                                  [  4.49890000e-06,   8.60220000e-06,  -2.38490000e-06],
                                  [  1.19114000e-05,   9.59500000e-06,   4.44540000e-06],
                                  [ -5.69520000e-06,  -1.03279000e-05,  -1.16304000e-05],
                                  [  1.04919000e-05,  -9.63280000e-06,   5.74100000e-06],
                                  [  8.30830000e-06,  -8.81250000e-06,   1.19956000e-05],
                                  [  3.77040000e-06,   1.52898000e-05,  -8.78300000e-06],
                                  [  9.89590000e-06,  -1.03254000e-05,   2.82040000e-06],
                                  [ -7.32077000e-05,   2.82500000e-06,   7.80527000e-05],
                                  [  3.53762000e-05,   6.30980000e-06,   7.29110000e-06],
                                  [ -4.39422000e-05,  -1.22764000e-05,   1.11221000e-05],
                                  [  4.06470000e-05,  -3.64624000e-05,   2.46980000e-06],
                                  [ -7.06660000e-05,   2.92506000e-05,   2.17727000e-05],
                                  [ -1.42704000e-05,   4.47619000e-05,  -4.80324000e-05],
                                  [ -2.59069000e-05,  -3.39819000e-05,   5.30350000e-06],
                                  [ -4.57860000e-06,  -1.44038000e-05,   4.75740000e-06],
                                  [  4.07596000e-05,  -9.04330000e-06,   1.24914000e-05],
                                  [  3.63805000e-05,   4.97230000e-06,  -2.90822000e-05],
                                  [ -2.22115000e-05,  -3.33703000e-05,  -7.52538000e-05]])
        self.stat01 = stats.matrix(self.matrix01)
        self.stat02 = stats.matrix(self.matrix02)
        #print self.stat01.get_stats()

    def test_check_statistics_matrix(self):
        # matrix 1
        self.assertEqual(self.stat01.get_mean(), 2.5)
        self.assertAlmostEqual(self.stat01.get_stdDev(), 1.11803398875, delta=1e-9)
        self.assertEqual(self.stat01.get_variance(), 1.25)
        self.assertAlmostEqual(self.stat01.get_RMSvalue(), 2.73861278753, delta=1e-9)
        self.assertEqual(self.stat01.get_maxAbs(), 4)
        self.assertEqual(self.stat01.get_minAbs(), 1)
        # matrix 2        
        self.assertAlmostEqual(self.stat02.get_mean(), -3.5994e-08, delta=1e-9)
        self.assertAlmostEqual(self.stat02.get_stdDev(), 2.93708886737e-05, delta=1e-9)
        self.assertAlmostEqual(self.stat02.get_variance(), 8.62649101483e-10, delta=1e-10)
        self.assertAlmostEqual(self.stat02.get_RMSvalue(), 2.93709107302e-05, delta=1e-9)
        self.assertAlmostEqual(self.stat02.get_maxAbs(), 7.8052699999999999e-05, delta=1e-9)
        self.assertAlmostEqual(self.stat02.get_minAbs(), 1.4501999999999999e-06, delta=1e-9)
        

if __name__ == '__main__':
    unittest.main()
