#!/usr/bin/env python
import molecule as mol
import sys, os
import numpy as np

def get_moleculeSet_benchmark_geomOpt():
    set = [mol.molecule('Histidine', nbAtomsInMolecule=20),
           mol.molecule('Ferrocene', nbAtomsInMolecule=21),
           mol.molecule('AT-basepair', nbAtomsInMolecule=30),
           mol.molecule('Penicillin', nbAtomsInMolecule=42),
           mol.molecule('Cu-complex', nbAtomsInMolecule=47),
           mol.molecule('Dibenzo-Crown18.6', nbAtomsInMolecule=50),
           mol.molecule('Tetracycline', nbAtomsInMolecule=56),
           mol.molecule('Beclomethasone', nbAtomsInMolecule=57),
           mol.molecule('c60_Ih', nbAtomsInMolecule=60),
           mol.molecule('Cholesterole', nbAtomsInMolecule=74),
           mol.molecule('CO-Heme', nbAtomsInMolecule=86),
           mol.molecule('c90_D5h', nbAtomsInMolecule=90),
           mol.molecule('CCCNa', nbAtomsInMolecule=90),
           mol.molecule('c100_D5d', nbAtomsInMolecule=100),
           mol.molecule('taxol', nbAtomsInMolecule= 113),
           mol.molecule('AGAGNaCl', nbAtomsInMolecule=150),
           mol.molecule('valinomycin', nbAtomsInMolecule=168),
           mol.molecule('vanomycin', nbAtomsInMolecule=176),
           mol.molecule('c180', nbAtomsInMolecule=180),
           mol.molecule('c240', nbAtomsInMolecule=240)]
           #mol.molecule('collagen-like-peptide',371),
           #mol.molecule('titin',392),
           #mol.molecule('crambin',642)]
    return set

def main():
    set = get_moleculeSet_benchmark_geomOpt()
    print set


if __name__ == "__main__":
    main()



