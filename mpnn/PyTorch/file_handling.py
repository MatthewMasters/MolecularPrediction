import numpy as np
import pandas as pd

def read_mol2(filename): # Read mol2 to obtain 
    atoms = []
    bonds = []
    fi = open(filename)
    atom_block = False
    bond_block = False
    for line in fi:
        if not atom_block:
            if line.find('@<TRIPOS>ATOM') != -1:
                atom_block = True
                continue
        if not bond_block:
            if line.find('@<TRIPOS>BOND') != -1:
                atom_block = False
                bond_block = True
                continue
            
        if atom_block:
            parts = line.split()
            atom_id = int(parts[0])
            atom_type = parts[5]
            charge = float(parts[8])
            x = float(parts[2])
            y = float(parts[3])
            z = float(parts[4])
            resn = parts[7]
            atoms.append([atom_id,atom_type,resn,charge,x,y,z])
            
        if bond_block:
            if line.find('@<TRIPOS>') != -1: break
            parts = line.split()
            bond_id = int(parts[0])
            atom_A = int(parts[1])
            atom_B = int(parts[2])
            bond_type = parts[3]
            bonds.append([bond_id,atom_A,atom_B,bond_type])
    
    atom_df = pd.DataFrame(atoms,columns=['atom_id','atom_type','resn','charge','x','y','z'])
    bond_df = pd.DataFrame(bonds,columns=['bond_id','atom_A','atom_B','bond_type'])
            
    return atom_df,bond_df

def read_pdb(filename):
    excl_atom = ['NA', 'Na', 'K']
    atoms = []
    bonds = []
    fi = open(filename)
    for line in fi:
        if line[:4] == 'ATOM' or line[:6] == 'HETATM':    
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            atom_id = int(line[6:11])
            atom_type = line[76:78].strip().upper()
            resn = line[17:20].strip()
            atom_idx = atom_indicies[atom_type]
            atoms.append([atom_id,resn,atom_idx,x,y,z])
        if line[:6] == 'CONECT':
            atom_id = line.split()[1]
            connected = line.split()[2:]
            bonds.append([atom_id,connected])
    atoms = pd.DataFrame(columns=['atom_id','resn','atom_type','x','y','z'],data=atoms)
    bonds = pd.DataFrame(columns=['atom_id','connected'],data=bonds)
    return atoms
