#!/usr/bin/env python

import sys, os
import re
import numpy as np
import molecule as mol


class moleculeInput(mol.molecule):
    def __init__(self, shortname="", name="", comments="",
                 regBasis=None, auxBasis=None, cabsBasis=None, jkBasis=None, admmBasis=None,
                 usingSymmetry="Nosymmetry",
                 unitDistance=None):
        mol.molecule.__init__(self, shortname, name="", comments="")
        self.regBasis = regBasis
        self.auxBasis = auxBasis
        self.admmBasis = admmBasis
        self.cabsBasis = cabsBasis
        self.jkBasis = jkBasis
        self.usingSymmetry = usingSymmetry
        self.listGroupSameAtoms = []
    def addGroupSameAtomInfo(self, groupAtoms):
        assert isinstance(groupAtoms,groupSameAtoms), 'Trying to add something which is not an groupSameAtoms object to a molecule object'
        self.listGroupSameAtoms.append(groupAtoms)
        for a in groupAtoms.listAtomsCoord:
            self.addAtomInfo(a)

    def __str__(self):
        s = ""
        #s += self.moleculeAsString()
        s += self.getContent_DALTON_MoleculeInput()
        return s

    def getContent_DALTON_MoleculeInput(self):
        #print "hello TEST"
        return self.getContent_DALTON_MoleculeInput_BASIS()


    def getContent_DALTON_MoleculeInput_BASIS(self):
        s = 'BASIS\n'
        if self.regBasis is None:
            s += 'regbasis Aux=auxbasis ADMM=ADMMbasis CABS=CABSbasis JK=JKbasis\n'
        else:
            if self.auxBasis is None:
                s += '{0} Aux=auxbasis ADMM=ADMMbasis CABS=CABSbasis JK=JKbasis\n'.format(self.regBasis)                
            else:
                if self.admmBasis is None:
                    s += '{0} Aux={1} ADMM=ADMMbasis CABS=CABSbasis JK=JKbasis\n'.format(self.regBasis,self.auxBasis)
                else:
                    s += '{0} Aux={1} ADMM={2} CABS=CABSbasis JK=JKbasis\n'.format(self.regBasis,self.auxBasis,self.admmBasis)

        s += '{0}\n'.format(self.name)
        s += '{0}\n'.format(self.comments)
        assert not self.unitDistance is None, 'Trying to print molecule infos without knowing the unitDistance variable'
        groups = self.create_groupsSameAtomsDALTON()
        s += 'Atomtypes={0:d} {1} {2}\n'.format(len(self.listGroupSameAtoms), self.unitDistance, self.usingSymmetry)
        s += self.getContent_DALTON_Molecule()
        return s

    def getContent_DALTON_MoleculeInput_ATOMBASIS(self):
        s = 'ATOMBASIS\n'
        s += '{0}\n'.format(self.name)
        s += '{0} {1}\n'.format(self.comments, self.comments)
        basisSets = ""
        if self.regBasis is None:
            basisSets += 'Basis=regbasis Aux=auxbasis ADMM=ADMMbasis CABS=CABSbasis JK=JKbasis\n'
        else:
            if self.auxBasis is None:
                basisSets += 'Basis={0} Aux=auxbasis ADMM=ADMMbasis CABS=CABSbasis JK=JKbasis\n'.format(self.regBasis)
            else:
                if self.admmBasis is None:
                    basisSets += 'Basis={0} Aux={1} ADMM=ADMMbasis CABS=CABSbasis JK=JKbasis\n'.format(self.regBasis,self.auxBasis)
                else:
                    basisSets += 'Basis={0} Aux={1} ADMM={2} CABS=CABSbasis JK=JKbasis\n'.format(self.regBasis,self.auxBasis,self.admmBasis)
        assert not self.unitDistance is None, 'Trying to print molecule infos without knowing the unitDistance variable'
        groups = self.create_groupsSameAtomsDALTON()
        s += 'Atomtypes={0:d} {1} {2}\n'.format(len(self.listGroupSameAtoms), self.unitDistance, self.usingSymmetry)
        for group in groups:
            s += 'Charge={0} Atoms={1:d} '.format(group.atomTypeCharge, group.nbAtomsInGroup)
            s += basisSets
            for a in group.listAtomsCoord:
                s += a.getContent_atomCoord() + "\n"
        return s

    def print_DALTON_MoleculeInput(self):
        self.print_DALTON_MoleculeInput_BASIS()
    def print_DALTON_MoleculeInput_BASIS(self):
        print '{0}'.format(self.getContent_DALTON_MoleculeInput_BASIS())
    def print_DALTON_MoleculeInput_ATOMBASIS(self):
        print '{0}'.format(self.getContent_DALTON_MoleculeInput_ATOMBASIS())


    def getContent_MoleculeInput(self):
        s=''
        for group in self.listGroupSameAtoms:
            s += '{0}'.format(group.getContent_DALTON_groupSameAtoms())
        return s
    def print_Molecule(self):
        print '{0}'.format(self.getContent_DALTON_Molecule())

    def create_groupsSameAtomsDALTON(self): # for creating DALTON inputs
        listUniqueSymbols = []
        groups = []
        # find the list of unique symbols used in the molecule
        for a in self.listAtoms:
            if not any(a.atomSymbol==s for s in listUniqueSymbols):
                listUniqueSymbols.append(a.atomSymbol)
        # create a group of atoms for each unique atom type in the molecule
        for s in listUniqueSymbols:
            newGroup = groupSameAtoms()
            for a in self.listAtoms:
                if a.atomSymbol==s:
                    newGroup.addAtomInfo(a)
            groups.append(newGroup)    
        self.listGroupSameAtoms = groups
        return groups

    def getContent_DALTON_Molecule(self):
        s = ''.join(['{0}'.format(group.getContent_DALTON_groupSameAtoms()) for group in self.listGroupSameAtoms])
        return s

class groupSameAtoms:
    def __init__(self):
        self.atomsSymbol = None
        self.atomTypeCharge = None
        self.nbAtomsInGroup = 0
        self.listAtomsCoord = []
    def addAtomInfo(self,atom):
        assert isinstance(atom,mol.atomInfos), 'Trying to add something which is not an atomInfos object to a groupSameAtoms object'
        self.atomsSymbol = atom.atomSymbol
        self.atomTypeCharge = atom.atomCharge
        self.nbAtomsInGroup += 1
        self.listAtomsCoord.append(atom)
    def setAtomTypeCharge(self, charge):
        self.atomTypeCharge = float(charge)
    def getContent_DALTON_groupSameAtoms(self):
        s = ''
#        s += 'Charge={0:g} Atoms={1:d}\n'.format(self.atomTypeCharge, self.nbAtomsInGroup)
        s += 'Charge={0} Atoms={1:d}\n'.format(self.atomTypeCharge, self.nbAtomsInGroup)
        for a in self.listAtomsCoord:
            s += a.getContent_atomCoord() + "\n"
        return s
    def print_DALTON_groupSameAtoms(self):
        print '{0}'.format(self.getContent_DALTON_groupSameAtoms())


def main():
    print "hello molecule!"

if __name__ == "__main__":
    main()



