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


def write_object_to_csv(myObj, csvOutputFilename):
    with open(csvOutputFilename, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])



def compare_csv_files(filename1, filename2, delimiter1=' ', delimiter2=' '):
    rows=[]
    with open(filename1, 'rb') as csvfile1:
        reader1 = csv.reader(csvfile1, delimiter=delimiter1, quotechar='|')
        with open(filename2, 'rb') as csvfile2:
            reader2 = csv.reader(csvfile2, delimiter=delimiter2, quotechar='|')
            for lhs, rhs in itertools.izip(reader1, reader2):
                if lhs != rhs:
                        rows.append(lhs)
                        rows.append(rhs)
    return rows

def write_2Darray_to_csv(rows, diffFileName):
    bool = False
    with open(diffFileName, 'wb') as csvfileW:
        writer1 = csv.writer(csvfileW, delimiter=',',
                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer1.writerows(rows)
        bool = True
    return bool
                        


# ============================================================================ #
# Testing
# ============================================================================ #
if __name__ == "__main__":
    filename1 = "./files/csvFile1.csv"
    filename2 = "./files/csvFile2.csv"
    diffFileName = './files/csv_difference.csv'
    diff = compare_csv_files(filename1, filename2, ',', ',')
    print diff
    diff = compare_csv_files(filename1, filename1, ',', ',')
    print diff
    #test = csv.reader(csvDiff, delimiter=',')
    #myObj
    #write_object_to_csv(myObj, csvOutputFilename)    
