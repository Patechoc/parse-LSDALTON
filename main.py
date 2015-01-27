#!/usr/bin/env python 

import sys, os, re
import argparse
import compare_LSDALTON_outputs as compLS

def compare():
    #rep = "./files/lsdalton_files/"
    #listFiles = [filename for filename in os.listdir(rep) if filename.endswith(".out")]
    #print 'Files present in', rep
    #print ''.join(f+"\n" for f in listFiles)
    
    parser = argparse.ArgumentParser(description='compare the gradients of two LSDALTON output files')
    parser.add_argument('filename01', type=str,
                        help='LSDALTON output file')
    parser.add_argument('filename02', type=str,
                        help='LSDALTON output file')
    args = parser.parse_args()
    comparison = compLS.get_compareInfoGradients(args.filename01,args.filename02)
    print comparison['matDiffGrad'].flatten()


if __name__ == "__main__":
    compare()

