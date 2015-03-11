#!/usr/bin/env python
import molecule
import sys, os
import numpy as np

def get_moleculeSet_benchmark_geomOpt():
    set = [molecule.molecule('Histidine', nbAtomsInMolecule=20),
           molecule.molecule('Ferrocene', nbAtomsInMolecule=21),
           molecule.molecule('AT-basepair', nbAtomsInMolecule=30),
           molecule.molecule('Penicillin', nbAtomsInMolecule=42),
           molecule.molecule('Cu-complex', nbAtomsInMolecule=47),
           molecule.molecule('Dibenzo-Crown18.6', nbAtomsInMolecule=50),
           molecule.molecule('Tetracycline', nbAtomsInMolecule=56),
           molecule.molecule('Beclomethasone', nbAtomsInMolecule=57),
           molecule.molecule('c60_Ih', nbAtomsInMolecule=60),
           molecule.molecule('Cholesterole', nbAtomsInMolecule=74),
           molecule.molecule('CO-Heme', nbAtomsInMolecule=86),
           molecule.molecule('c90_D5h', nbAtomsInMolecule=90),
           molecule.molecule('CCCNa', nbAtomsInMolecule=90),
           molecule.molecule('c100_D5d', nbAtomsInMolecule=100),
           molecule.molecule('taxol', nbAtomsInMolecule= 113),
           molecule.molecule('AGAGNaCl', nbAtomsInMolecule=150),
           molecule.molecule('valinomycin', nbAtomsInMolecule=168),
           molecule.molecule('vanomycin', nbAtomsInMolecule=176),
           molecule.molecule('c180', nbAtomsInMolecule=180),
           molecule.molecule('c240', nbAtomsInMolecule=240)]
           #molecule('collagen-like-peptide',371),
           #molecule('titin',392),
           #molecule('crambin',642)]
    return set

def main():
    set = get_moleculeSet_benchmark_geomOpt()
    print set


if __name__ == "__main__":
    main()



