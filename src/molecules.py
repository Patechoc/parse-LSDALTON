#!/usr/bin/env python

import sys, os
import numpy as np

# ============================================================================ #
# Class: MOLECULE
# ============================================================================ #
class molecule(object):
    def __init__(self, shortname="", nb_atoms=-1, name="", coord_cartes=""):
        self.name = name
        self.shortname = shortname
        self.nb_atoms = int(nb_atoms)
        self.coord_cartes = coord_cartes
        if (name.strip() == ""):
            self.name = shortname
    def __repr__(self):
        return self.shortname+"({:d}".format(self.nb_atoms)+")"


def get_moleculeSet_benchmark_geomOpt():
    set = [molecule('Histidine',20),
           molecule('Ferrocene',21),
           molecule('AT-basepair',30),
           molecule('Penicillin',42),
           molecule('Cu-complex',47),
           molecule('Dibenzo-Crown18.6',50),
           molecule('Tetracycline',56),
           molecule('Beclomethasone',57),
           molecule('c60_Ih',60),
           molecule('Cholesterole',74),
           molecule('CO-Heme',86),
           molecule('c90_D5h',90),
           molecule('CCCNa',90),
           molecule('c100_D5d',100),
           molecule('taxol', 113),
           molecule('AGAGNaCl',150),
           molecule('valinomycin',168),
           molecule('vanomycin',176),
           molecule('c180',180),
           molecule('c240',240)]
           #molecule('collagen-like-peptide',371),
           #molecule('titin',392),
           #molecule('crambin',642)]
    return set

def main():
    set = get_moleculeSet_benchmark_geomOpt()
    print set


if __name__ == "__main__":
    main()



