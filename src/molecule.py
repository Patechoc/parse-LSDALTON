#!/usr/bin/env python

import sys, os
import re
import numpy as np



Atomic_NUMBERS = {"H": 1,"He": 2,
                  "Li": 3,"Be": 4,"B": 5,"C": 6,"N": 7,"O": 8,"F": 9,"Ne": 10,
                  "Na": 11,"Mg": 12,"Al": 13,"Si": 14,"P": 15,"S": 16,"Cl": 17,"Ar": 18,
                  "K": 19,"Ca": 20,"Sc": 21,"Ti": 22,"V": 23,"Cr": 24,"Mn": 25,"Fe": 26,"Co": 27,"Ni": 28,"Cu": 29,"Zn": 30,"Ga": 31,"Ge": 32,"As": 33,"Se": 34,"Br": 35,"Kr": 36,
                  "Rb": 37,"Sr": 38,"Y": 39,"Zr": 40,"Nb": 41,"Mo": 42,"Tc": 43,"Ru": 44,"Rh": 45,"Pd": 46,"Ag": 47,"Cd": 48,"In": 49,"Sn": 50,"Sb": 51,"Te": 52,"I": 53,"Xe": 54,
                  "Cs": 55,"Ba": 56,"La": 57,"Hf": 72,"Ta": 73,"W": 74,"Re": 75,"Os": 76,"Ir": 77,"Pt": 78,"Au": 79,"Hg": 80,"Tl": 81,"Pb": 82,"Bi": 83,"Po": 84,"At": 85,"Rn": 86,
                  "Fr": 87,"Ra": 88,"Ac": 89,"Ku": 104,"Ha": 105}


class atomInfos(object):
    bohr_in_angstrom = 0.5291772083
    def __init__(self, atomSymbol,
                 xCoord, yCoord, zCoord,
                 atomCharge=None,
                 unitDistances=None):
        self.atomSymbol = atomSymbol
        if atomCharge is None: 
            self.atomCharge = float(Atomic_NUMBERS[atomSymbol])
        else:
            self.atomCharge = float(atomCharge)
        self.unitDistances = unitDistances
        self.xCoord = float(xCoord)
        self.yCoord = float(yCoord)
        self.zCoord = float(zCoord)
    def setSymbol(self, symbol):
        self.atomSymbol = symbol
    def setCharge(self, charge):
        self.atomCharge = float(charge)
    def setAtomCoord(self, x,y,z):
        self.xCoord = float(x)
        self.yCoord = float(y)
        self.zCoord = float(z)
    def getContent_atomCoord(self, newUnitDistance=None):
        s = ''
        if newUnitDistance != None:
            if  re.match(newUnitDistance, self.unitDistances, re.I):
                s += '{0:s}     {1: 7.14f}     {2: 7.14f}     {3: 7.14f}\n'.format(self.atomSymbol, self.xCoord, self.yCoord, self.zCoord)
            elif re.match("bohr", newUnitDistance, re.I) and re.match("angstrom", self.unitDistances, re.I):
                #1 bohr=0.5291772083 Angstrom
                s += '{0:s}     {1: 7.14f}     {2: 7.14f}     {3: 7.14f}\n'.format(self.atomSymbol, self.xCoord/bohr_in_angstrom, self.yCoord/bohr_in_angstrom, self.zCoord/bohr_in_angstrom)
            elif re.match("angstrom", newUnitDistance, re.I) and re.match("bohr", self.unitDistances, re.I):
                #1 bohr=0.5291772083 Angstrom
                s += '{0:s}     {1: 7.14f}     {2: 7.14f}     {3: 7.14f}\n'.format(self.atomSymbol, self.xCoord*.5291772083, self.yCoord*bohr_in_angstrom, self.zCoord*bohr_in_angstrom)
        else:
            s += '{0:s}     {1: 7.14f}     {2: 7.14f}     {3: 7.14f}\n'.format(self.atomSymbol, self.xCoord, self.yCoord, self.zCoord)
        return s
    def print_atomCoord(self):
        print '{0}'.format(self.getContent_atomCoord())


class groupSameAtoms(object):
    def __init__(self):
        self.atomsSymbol = None
        self.atomTypeCharge = None
        self.nbAtomsInGroup = 0
        self.listAtomsCoord = []
    def addAtomInfo(self,atom):
        assert isinstance(atom,atomInfos), 'Trying to add something which is not an atomInfos object to a groupSameAtoms object'
        self.atomsSymbol = atom.atomSymbol
        self.atomTypeCharge = atom.atomCharge
        self.nbAtomsInGroup += 1
        self.listAtomsCoord.append(atom)
    def setAtomTypeCharge(self, charge):
        self.atomTypeCharge = float(charge)
    def getContent_DALTON_groupSameAtoms(self):
        s = ''
        s += 'Charge={0} Atoms={1:d}\n'.format(self.atomTypeCharge, self.nbAtomsInGroup)
        for a in self.listAtomsCoord:
            s += a.getContent_atomCoord()
        return s
    def print_DALTON_groupSameAtoms(self):
        print '{0}'.format(self.getContent_DALTON_groupSameAtoms())


class molecule(object):
    def __init__(self, shortname, name="", comments="", nbAtomsInMolecule=-1, unitDistances=None):
        self.name = name
        self.shortname = shortname
        if (name.strip() == ""):
            self.name = shortname
        self.nbAtomsInMolecule = int(nbAtomsInMolecule)
        self.unitDistances = unitDistances
        self.comments = comments
        self.listAtoms          = []
        self.listGroupSameAtoms = []
    def setUnitDistances(self,unitDistances):
        self.unitDistances = unitDistances
    def addGroupSameAtomInfo(self, groupAtoms):
        assert isinstance(groupAtoms,groupSameAtoms), 'Trying to add something which is not an groupSameAtoms object to a molecule object'
        self.listGroupSameAtoms.append(groupAtoms)
        for a in groupAtoms.listAtomsCoord:
            self.addAtomInfo(a)
    def addAtomInfo(self,atom):
        self.nbAtomsInMolecule += 1
        assert isinstance(atom,atomInfos), 'Trying to add something which is not an atomInfos object to a molecule object'
        self.listAtoms.append(atom)
        if not atom.unitDistances is None: # assuming that all atoms with unitDistance defined have actually the same :)
            self.setUnitDistances(atom.unitDistances)
    def __str__(self):
        return self.shortname

def main():
    print "hello molecule!"

if __name__ == "__main__":
    main()
