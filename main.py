# ============================================================================ #
# Imports
# ============================================================================ #
import sys, os, re
from glob import glob
from subprocess import check_output
import parserGrammar
import csv

# http://pandas.pydata.org/

#with open('input.txt') ad f:
    #data = [map(int, row) for row in csv.reader(f)]
def main():
    rep = "./files/lsdalton_files/"
    listFiles = [filename for filename in os.listdir(rep) if filename.endswith(".out")]
    print 'Files present in', rep
    print ''.join(f+"\n" for f in listFiles)
    

if __name__ == "__main__":
    main()

