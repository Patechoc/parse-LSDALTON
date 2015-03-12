#!/usr/bin/env python

import sys, os
import re
import numpy as np
import numpy.testing as npt
import molecule as mol

class calculation(object):
    def __init__(self, molecule=None, calculationInput=None, calculationOutput=None):
        assert isinstance(molecule, mol.molecule), \
            "%r is not a 'molecule' object" % molecule
        self.molecule          = molecule
        self.calculationInput  = calculationInput
        self.calculationOutput = calculationOutput


def main():
    print "hello calculation!"

if __name__ == "__main__":
    main()
