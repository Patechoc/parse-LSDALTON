#!/usr/bin/env python
import molecule
import sys, os
import numpy as np

def get_moleculeSet_benchmark_geomOpt():
    set = [molecule('Histidine', nbAtomsInMolecule=20),
           molecule('Ferrocene', nbAtomsInMolecule=21),
           molecule('AT-basepair', nbAtomsInMolecule=30),
           molecule('Penicillin', nbAtomsInMolecule=42),
           molecule('Cu-complex', nbAtomsInMolecule=47),
           molecule('Dibenzo-Crown18.6', nbAtomsInMolecule=50),
           molecule('Tetracycline', nbAtomsInMolecule=56),
           molecule('Beclomethasone', nbAtomsInMolecule=57),
           molecule('c60_Ih', nbAtomsInMolecule=60),
           molecule('Cholesterole', nbAtomsInMolecule=74),
           molecule('CO-Heme', nbAtomsInMolecule=86),
           molecule('c90_D5h', nbAtomsInMolecule=90),
           molecule('CCCNa', nbAtomsInMolecule=90),
           molecule('c100_D5d', nbAtomsInMolecule=100),
           molecule('taxol', nbAtomsInMolecule= 113),
           molecule('AGAGNaCl', nbAtomsInMolecule=150),
           molecule('valinomycin', nbAtomsInMolecule=168),
           molecule('vanomycin', nbAtomsInMolecule=176),
           molecule('c180', nbAtomsInMolecule=180),
           molecule('c240', nbAtomsInMolecule=240)]
           #molecule('collagen-like-peptide',371),
           #molecule('titin',392),
           #molecule('crambin',642)]
    return set

def main():
    set = get_moleculeSet_benchmark_geomOpt()
    print set


if __name__ == "__main__":
    main()



