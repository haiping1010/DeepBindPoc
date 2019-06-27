import pandas as pd
import numpy as np
from pandas import DataFrame
from glob import glob
import sys
from time import time
path = sys.argv[1]
mp_data=sys.argv[2]
l_files = glob(path +  '/*.csv')

t = pd.read_csv(l_files[0])
lc = t.columns[2:]

l_len = len(l_files)
ligands = DataFrame(columns = lc)


for l in l_files:
    t = pd.read_csv(l)
    ligands = ligands.append(t.ix[:, 2:], ignore_index = True)
    print(t.shape, t.ix[0, 2], l)

#print(ligands.shape)
#print(l_len)
p_files = glob('all_pocket' +'/*_pocVec.txt')
p_len = len(p_files)
proteins = DataFrame()

for i, p in enumerate(p_files):
    #print(i * 1.0 / p_len)
    f = open(p)
    t = f.read()
    t = t[:-1].replace('[ ', '').replace('[', '').replace('\n', '').split()
    t.insert(0, p.split('/')[-1].split('.')[0])
    t = DataFrame(np.array(t).reshape(1, -1))
    if t.shape == (1, 301):
        proteins = proteins.append(t, ignore_index=True)
    else:
        print(t.shape, p)



ligands.to_hdf(mp_data+'/ligands.h5', 'df')

proteins.to_hdf(mp_data+'/proteins.h5', 'df')


ligands = pd.read_hdf(mp_data+'/ligands.h5', 'df')
proteins = pd.read_hdf(mp_data+'/proteins.h5', 'df')


print(ligands.shape)
#print(l_len)
print(proteins.shape)

#print(p_len)
############################################
############################################
pos = DataFrame()
pos_list_used = []


'''
ligands_n = DataFrame(columns = lc)
for i in range(proteins.shape[0]):
    protein = proteins.ix[i:i, 1:]
    pname = proteins.ix[:, 0][i].split('_')[0]
    print pname
    ligand_n = ligands[ligands.ix[:, 0] == pname+'_GTP_ligands_n.pdb'].ix[:, 1:]
    ##compound=bind(pname,pname) 
    ligands_n = ligands_n.append(ligand_n, ignore_index = True)
'''
ligands_n = pd.DataFrame(np.repeat(ligands.values, proteins.shape[0], axis=0))

proteins = pd.DataFrame(np.array(proteins.values))

#proteins = pd.DataFrame(np.vstack((proteins.values, proteins.values)))

ligand = ligands_n.ix[:, 1:]
protein = proteins.ix[:, 1:]
for i in range(proteins.shape[0]):
    pname = proteins.ix[i, 0]
    lname = ligands_n.ix[i, 0].replace('_ligand.pdb','')
    pos_list_used.append(lname+pname[4:])
print protein.shape
print ligand.shape



compound = DataFrame(np.hstack((protein, ligand)))
pos = pos.append(compound, ignore_index = True)

pos.to_hdf(mp_data+'/pos.h5', 'df')

pos_read = pd.read_hdf(mp_data+'/pos.h5', 'df')
pos_list_used = DataFrame(pos_list_used)
pos_list_used.to_csv(mp_data+'/pos_list.csv', index = False, header = ['name'])
pos_list_used.head()



