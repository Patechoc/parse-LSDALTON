#!/usr/bin/env python 

import unittest
import lib_spreadsheet as libCSV
import numpy as np

# http://docs.python-guide.org/en/latest/writing/tests/


class csv_test(unittest.TestCase):

    def setUp(self):
        self.seq = list(range(10))
        self.filename1 = "./files/csvFile1.csv"
        self.filename2 = "./files/csvFile2.csv"
        self.diffFileName = './files/csv_difference.csv'

    def test_compare_identical_csv_files(self):
        diff = libCSV.compare_csv_files(self.filename1, self.filename1, ',', ',') 
        self.assertTrue(diff == [])

    def test_compare_different_csv_files(self):
        diff = libCSV.compare_csv_files(self.filename1, self.filename2, ',', ',') 
        self.assertEqual(diff, [['1997', 'Ford', 'E350','"ab', ' abs', ' moon"', '3000.00'],
                                ['1997', 'Ford', 'E350', '"ac', ' abs', ' moon"', '3000.00'],
                                ['2010', 'BMW', 'Touran', '"MUST SELL!'],
                                ['1996', 'Jeep', 'Grand Cherokee', '"MUST SELL!']])


if __name__ == '__main__':
    unittest.main()
