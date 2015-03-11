#!/usr/bin/env python

import sys, os
import re
import numpy as np
import molecule



class moleculeInput_DALTON(molecule):
    def __init__(self, moleculeInfo, comments="", 
                 regBasis=None, auxBasis=None, cabsBasis=None, jkBasis=None, admmBasis=None,
                 usingSymmetry="Nosymmetry",
                 unitDistances=None):
        assert isinstance(moleculeInfo,molecule), 'Trying to add something which is not a moleculeInfo object to a moleculeInput object'
        self.moleculeInfo = moleculeInfo
        self.regBasis = regBasis
        self.auxBasis = auxBasis
        self.admmBasis = admmBasis
        self.cabsBasis = cabsBasis
        self.jkBasis = jkBasis
        self.comments = comments
        self.usingSymmetry = usingSymmetry

    def getContent_DALTON_Molecule(self):
        s=''
        for group in self.listGroupSameAtoms:
            s += '{0}'.format(group.getContent_DALTON_groupSameAtoms())
        return s
    def print_DALTON_Molecule(self):
        print '{0}'.format(self.getContent_DALTON_Molecule())
    def getContent_MOLCAS_Molecule(self):
        s=''
        for atom in self.listAtoms:
            s += '{0}'.format(atom.getContent_atomCoord())
        return s
    def print_MOLCAS_Molecule(self):
        print '{0}'.format(self.getContent_MOLCAS_Molecule())
    def getContent_XYZ_Molecule(self):
        s=''
        for atom in self.listAtoms:
            s += '{0}'.format(atom.getContent_atomCoord("Angstrom"))
        return s
    def print_XYZ_Molecule(self):
        print '{0}'.format(self.getContent_XYZ_Molecule())
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



class moleculeInput:
    def __init__(self,molecule,comments="",usingSymmetry="Nosymmetry",regBasis=None,auxBasis=None,cabsBasis=None,jkBasis=None,admmBasis=None):
        assert isinstance(molecule,moleculeInfo), 'Trying to add something which is not a moleculeInfo object to a moleculeInput object'
        self.molecule = molecule
        self.regBasis = regBasis
        self.auxBasis = auxBasis
        self.admmBasis = admmBasis
        self.cabsBasis = cabsBasis
        self.jkBasis = jkBasis
        self.comments = comments
        self.usingSymmetry = usingSymmetry
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
                s += '{0} Aux={1} ADMM=ADMMbasis CABS=CABSbasis JK=JKbasis\n'.format(self.regBasis,self.auxBasis)                
        s += '{0}\n'.format(self.molecule.name)
        s += '{0} {1}\n'.format(self.comments, self.molecule.comments)
        assert not self.molecule.unitDistances is None, 'Trying to print molecule infos without knowing the unitDistance variable'
        groups = self.molecule.create_groupsSameAtomsDALTON()
        s += 'Atomtypes={0:d} {1} {2}\n'.format(len(self.molecule.listGroupSameAtoms), self.molecule.unitDistances, self.usingSymmetry)
        s += self.molecule.getContent_DALTON_Molecule()
        return s
    def getContent_DALTON_MoleculeInput_ATOMBASIS(self):
        s = 'ATOMBASIS\n'
        s += '{0}\n'.format(self.molecule.name)
        s += '{0} {1}\n'.format(self.comments, self.molecule.comments)
        basisSets = ""
        if self.regBasis is None:
            basisSets += 'Basis=regbasis Aux=auxbasis ADMM=ADMMbasis CABS=CABSbasis JK=JKbasis\n'
        else:
            if self.auxBasis is None:
                basisSets += 'Basis={0} Aux=auxbasis ADMM=ADMMbasis CABS=CABSbasis JK=JKbasis\n'.format(self.regBasis)                
            else:
                basisSets += 'Basis={0} Aux={1} ADMM=ADMMbasis CABS=CABSbasis JK=JKbasis\n'.format(self.regBasis,self.auxBasis)                
        assert not self.molecule.unitDistances is None, 'Trying to print molecule infos without knowing the unitDistance variable'
        groups = self.molecule.create_groupsSameAtomsDALTON()
        s += 'Atomtypes={0:d} {1} {2}\n'.format(len(self.molecule.listGroupSameAtoms), self.molecule.unitDistances, self.usingSymmetry)
        for group in groups:
            s += 'Charge={0} Atoms={1:d} '.format(group.atomTypeCharge, group.nbAtomsInGroup)
            s += basisSets
            for a in group.listAtomsCoord:
                s += a.getContent_atomCoord()
        return s

    def print_DALTON_MoleculeInput(self):
        self.print_DALTON_MoleculeInput_BASIS()
    def print_DALTON_MoleculeInput_BASIS(self):
        print '{0}'.format(self.getContent_DALTON_MoleculeInput_BASIS())
    def print_DALTON_MoleculeInput_ATOMBASIS(self):
        print '{0}'.format(self.getContent_DALTON_MoleculeInput_ATOMBASIS())
    def print_MOLCAS_MoleculeInput(self):
        print '{0}'.format(self.getContent_MOLCAS_MoleculeInput())
    def getContent_MOLCAS_MoleculeInput(self):
        s=''
        s += '{0:d}\n'.format(self.molecule.nbAtomsInMolecule)
        if self.molecule.unitDistances is None:
            s += '{0}\n'.format(self.molecule.name)
        else:
            s += '{0} (in {1})\n'.format(self.molecule.name,self.molecule.unitDistances)
        s += self.molecule.getContent_MOLCAS_Molecule()
        s += '\n'
        return s
    def print_XYZ_MoleculeInput(self):
        print '{0}'.format(self.getContent_XYZ_MoleculeInput())
    def getContent_XYZ_MoleculeInput(self):
        s=''
        s += '{0:d}\n'.format(self.molecule.nbAtomsInMolecule)
        if self.molecule.unitDistances is None:
            #s += '{0}\n'.format(self.molecule.name)
            print "can't convert the molecule, the input for the distance unit is unknown"
            return None
        else:
            if re.match("angstrom",self.molecule.unitDistances,re.IGNORECASE):
                s += '{0} (from input already in {1})\n'.format(self.molecule.name,self.molecule.unitDistances)
            elif re.match("bohr",self.molecule.unitDistances,re.IGNORECASE):
                s += '{0} (converted to Angstrom from input in {1})\n'.format(self.molecule.name,self.molecule.unitDistances)
            else:
                print "can't convert the molecule, the input for the distance unit is neither Bohr or Angstrom"
                return None
            s += self.molecule.getContent_XYZ_Molecule()
            s += '\n'
        return s



def main():
    print "hello molecule!"

if __name__ == "__main__":
    main()



