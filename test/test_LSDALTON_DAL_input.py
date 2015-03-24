#!/usr/bin/env python 

import unittest
import LSDALTON_DAL_input as LSdal
import numpy as np

# http://docs.python-guide.org/en/latest/writing/tests/
# http://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure

class LSDALTON_DAL_input_test(unittest.TestCase):

    def setUp(self):
      self.str = """**GENERAL
                    .TIME
                    .NOGCBASIS
                    **OPTIMIZE
                    .MAX IT
                    1000
                    .LOOSE
                    .REDINT
                    .INIMOD
                    **INTEGRALS
                    .DENSFIT
                    .THRESH
                    1.0D-14
                    **WAVE FUNCTIONS
                    .DFT
                    B3LYP
                    *DENSOPT
                    .VanLenthe
                    .RESTART
                    .MAXIT
                    500
                    *DFT INPUT
                    .GRID5
                    *END OF INPUT"""
        
    def test_parse_from_string(self):
      str = self.str
      keywords = LSdal.get_keywords(str)
      #print keywords
      #headlines = LSdal.get_headlines(keywords)
      self.assertEqual(keywords.name,"ROOT") 

if __name__ == '__main__':
    unittest.main()
