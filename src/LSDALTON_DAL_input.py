#!/usr/bin/env python 

import sys, os, re, math
import numpy as np
import subprocess as subproc
import parser


		
def get_keywords(str):
	keywords = keyword() # ROOT element
	## terminate with "*END OF INPUT"
	## split the string using headlines ("**" followed by "GENERAL", "INTEGRAL", "WAVEFUNCTION", "OPTIMIZE", "DYNAMI", "LOCALIZE ORBITALS", "RESPONS", "DEC", "CC", "PLT", "PLTGRID")
	## split headlines in sections and their respective parameters/values
	return keywords

def build_DAL_input_from_string(str, name=""):
	dal = DAL_input()
	dal.inputString = str
	dal.keywords = get_keywords(str)

	return dal

def build_DAL(filepath, name=""):
	# name = filename or specified name as argument
	# get string from file
	str = ""
	dal = build_DAL_input_from_string(str, name)
	return dal	



# ============================================================================ #
# Class: DAL_input
# ============================================================================ #
class DAL_input(object):
    def __init__(self):
        self.inputString  = None
        self.QMmethod     = None        # HF/DFT/CC...
        self.isGeomOpt    = False       # using **OPTIMIZE or not
        self.keywords     = keywords    # Tree of keywords with (branches and leaves as in XML) headlines (**GENERAL, **INTEGRAL, ...) and their sections (**GENERAL/.TIME, **GENERAL/.NOGCBASIS, ...)

# ============================================================================ #
# Class: keyword
# ============================================================================ #
class keyword(object):
    def __init__(self, name="ROOT"):
        self.name        = str(name)        # e.g. **GENERAL, **INTEGRAL, ... NOGCBASIS, ...
        self.description = ""          # short text description of the keyword
        self.value       = None        # None if not relevant, or the value of a parameters choice (e.g. the "<Print level>" for the keyword ".BASPRINT")
        self.valueFormat = None        # None if not relevant, or format of the parameter value is needed (e.g. "GGAKey HF=0.2 Slater=0.8 Becke=0.72 LYP=0.81 VWN=0.19" for the keyword ".DFT")
        self.defaultValueIfnotSet = None
        self.parent      = "ROOT"      # "ROOT" for headlines like "**GENERAL, **INTEGRAL" ..., and another keywords for the others
        self.children    = None        # list of keywords below this headlines/section
        self.mandatory   = True        # Boolean: True of False

	def __repr__(self):
		#return self.name+" ("+self.description+")" + "\nparent:"+self.parent
		return str(self.name)

	def __str__(self):
		#return self.name+" ("+self.description+")" + "\nparent:"+self.parent
		return str(self.name)

	def set_keyword(self, name, description="", value="", parent="ROOT", mandatory=True, valueFormat=None, defaultValueIfnotSet=None):
		self.name        = name        # e.g. **GENERAL, **INTEGRAL, ... NOGCBASIS, ...
		self.description = description # short text description of the keyword
		self.value       = value       # None if not relevant, or the value of a parameters choice (e.g. the "<Print level>" for the keyword ".BASPRINT")
		self.valueFormat = valueFormat # None if not relevant, or format of the parameter value is needed (e.g. "GGAKey HF=0.2 Slater=0.8 Becke=0.72 LYP=0.81 VWN=0.19" for the keyword ".DFT")
		self.defaultValueIfnotSet = defaultValueIfnotSet
		self.parent      = "ROOT"      # "ROOT" for headlines like "**GENERAL, **INTEGRAL" ..., and another keywords for the others
		self.children    = children    # list of keywords below this headlines/section
		self.mandatory   = mandatory   # Boolean: True of False



def main():
	keywords = keyword()
	print keywords.name

# ============================================================================ #
# Testing
# ============================================================================ #
if __name__ == "__main__":
	main()