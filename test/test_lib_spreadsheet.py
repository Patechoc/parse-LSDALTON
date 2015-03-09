#!/usr/bin/env python 

import unittest
import lib_spreadsheet as libCSV
import numpy as np

# http://docs.python-guide.org/en/latest/writing/tests/


class csv_test(unittest.TestCase):

    def setUp(self):
        self.seq = list(range(10))
        self.filename1 = "../files/csvFile1.csv"
        self.filename2 = "../files/csvFile2.csv"
        self.filename3 = "../files/writtenObj.csv"
        self.filename4 = "../files/writtenObjArray.csv"
        self.diffFileName = '../files/csv_difference.csv'

    def test_compare_identical_csv_files(self):
        diff = libCSV.compare_csv_files(self.filename1, self.filename1, ',', ',') 
        self.assertTrue(diff == [])

    def test_compare_different_csv_files(self):
        diff = libCSV.compare_csv_files(self.filename1, self.filename2, ',', ',') 
        self.assertEqual(diff, [['1997', 'Ford', 'E350','"ab', ' abs', ' moon"', '3000.00'],
                                ['1997', 'Ford', 'E350', '"ac', ' abs', ' moon"', '3000.00'],
                                ['2010', 'BMW', 'Touran', '"MUST SELL!'],
                                ['1996', 'Jeep', 'Grand Cherokee', '"MUST SELL!']])
    def test_write_Object_to_csv_file(self):
        myObj={'FAMILY NAME':'Doe', 'FIRST NAME':'John', 'AGE':'35', 'NATIONALITY':'american', 'License':'B'}
        newFile = libCSV.write_object_to_csv(myObj, '../files/writeObj.csv', delimiterW=',', quotecharW='"')
        diff = libCSV.compare_csv_files('../files/writeObj.csv', self.filename3, ',', ',') 
        self.assertTrue(diff == [])

    def test_write_arrayOfObjects_to_csv_file(self):
        myObjArray=[{'FAMILY NAME':'Doe', 'FIRST NAME':'John', 'AGE':'35', 'NATIONALITY':'american', 'License':'B'},
                    {'FAMILY NAME':'Merlot', 'FIRST NAME':'Patrick', 'AGE':'35', 'NATIONALITY':'french', 'License':'B'},
                    {'FAMILY NAME':'Obama', 'FIRST NAME':'Barak', 'AGE':'62', 'NATIONALITY':'american', 'License':'B'},
                    {'FAMILY NAME':'Hollande', 'FIRST NAME':'Francois', 'AGE':'64', 'NATIONALITY':'french', 'License':'B'}]
        newFile = libCSV.write_arrayOfObjects_to_csv(myObjArray, '../files/writeObjArray.csv', delimiterW=',', quotecharW='"')
        diff = libCSV.compare_csv_files('../files/writeObjArray.csv', self.filename4, ',', ',') 
        self.assertTrue(diff == [])


if __name__ == '__main__':
    unittest.main()
