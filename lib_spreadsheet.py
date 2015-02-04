#!/usr/bin/env python 

import sys, os, re, math
import numpy as np
import csv
import itertools
#from glob import glob
#import subprocess as subproc
# http://pandas.pydata.org/

#with open('input.txt') ad f:
    #data = [map(int, row) for row in csv.reader(f)]


def write_object_to_csv(myObj):
    with open('eggs.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

def compare_csv_files(filename1, filename2):
    with open(filename1, 'rb') as csvfile:
        reader1 = csv.reader(filename1)

        with open(filename2, 'rb') as csvfile:
            reader2 = csv.reader(filename2)
            with open('difference.csv', 'wb') as csvfile:
                writer1 = csv.writer(csvfile)
                for lhs, rhs in itertools.izip(reader1, reader2):
                    if lhs != rhs:
                        print "lhs",lhs
                        print "reader1(lhs)",reader1(lhs)
                        print "rhs",rhs
                        writer1.writerow(lhs)
                        writer1.writerow(rhs)
                return writer1



# ============================================================================ #
# Testing
# ============================================================================ #
if __name__ == "__main__":
    filename1 = "./files/csvFile1.csv"
    filename2 = "./files/csvFile2.csv"
    compare_csv_files(filename1, filename2)
    
