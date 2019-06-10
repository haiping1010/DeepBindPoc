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
#l_files = glob(path +  '/*.csv')

#l_files = glob(path +  '/'+ mp_data.replace('mp_data_','')  +'*.csv')
l_len = len(l_files)
ligands = DataFrame(columns = lc)


'''
for l in l_files:
    t = pd.read_csv(l)
    ligands = ligands.append(t.ix[:, 2:], ignore_index = True)
    print(t.shape, t.ix[0, 2], l)

#print(ligands.shape)
#print(l_len)

p_files = glob('all_pos_poc' +'/*_pocVec.txt')
p_len = len(p_files)
proteins = DataFrame()

for i, p in enumerate(p_files):
    print(i * 1.0 / p_len)
    f = open(p)
    t = f.read()
    t = t[:-1].replace('[ ', '').replace('[', '').replace('\n', '').split()
    t.insert(0, p.split('/')[-1].split('.')[0])
    t = DataFrame(np.array(t).reshape(1, -1))
    if t.shape == (1, 301):
        proteins = proteins.append(t, ignore_index=True)
    else:
        print(t.shape, p)


p_files_neg = glob('all_neg_poc_clean' +'/*_pocVec.txt')
p_len_neg = len(p_files_neg)
proteins_neg = DataFrame()

for i, p in enumerate(p_files_neg):
    #print(i * 1.0 / p_len)
    f = open(p)
    t = f.read()
    t = t[:-1].replace('[ ', '').replace('[', '').replace('\n', '').split()
    t.insert(0, p.split('/')[-1].split('.')[0])
    t = DataFrame(np.array(t).reshape(1, -1))
    if t.shape == (1, 301):
        proteins_neg = proteins_neg.append(t, ignore_index=True)
    else:
        print(t.shape, p)


#print(proteins.shape)
#print(p_len)
#np.sum(np.sum(proteins.isna()))

ligands.to_hdf(mp_data+'/ligands.h5', 'df')

proteins.to_hdf(mp_data+'/proteins.h5', 'df')


proteins_neg.to_hdf(mp_data+'/proteins_neg_clean.h5', 'df')

'''


ligands = pd.read_hdf(mp_data+'/ligands.h5', 'df')
proteins = pd.read_hdf(mp_data+'/proteins.h5', 'df')
proteins_neg = pd.read_hdf(mp_data+'/proteins_neg_clean.h5', 'df')


print(ligands.shape)
#print(l_len)
print(proteins.shape)
print(proteins_neg.shape)

#print(p_len)
############################################
############################################
#proteins.head()
#proteins.head()
##t = np.hstack((tp, tl))
##pos = DataFrame()
##pos = pos.append(DataFrame(t))
pos = DataFrame()
pos_list_used = []
neg = DataFrame()
neg_list_used = []



'''
def bind(pname, lname):
    protein = proteins[proteins.ix[:, 0] == pname+'_pocket_n.pdb_pocVec.txt'].ix[:, 1:]
    ligand = ligands[ligands.ix[:, 0] == lname+'_ligand'].ix[:, 1:]
    compound = DataFrame(np.hstack((protein, ligand)))
    return compound
'''


ligands_n = DataFrame(columns = lc)
for i in range(proteins.shape[0]):
    protein = proteins.ix[i:i, 1:]
    pname = proteins.ix[:, 0][i].split('_')[0]
    ligand_n = ligands[ligands.ix[:, 0] == pname+'_ligand'].ix[:, 1:]
    ##compound=bind(pname,pname) 
    ligands_n = ligands_n.append(ligand_n, ignore_index = True)

ligand = ligands_n.ix[:, 1:]
protein = proteins.ix[:, 1:]
for i in range(proteins.shape[0]):
    pname = proteins.ix[i, 0]
    pos_list_used.append(pname)
print protein.shape
print ligand.shape

compound = DataFrame(np.hstack((protein, ligand)))
pos = pos.append(compound, ignore_index = True)



ligands_n_neg = DataFrame(columns = lc)
for i in range(proteins_neg.shape[0]):
    protein = proteins_neg.ix[i:i, 1:]
    pname = proteins_neg.ix[:, 0][i].split('_')[0]
    ligand_n_neg = ligands[ligands.ix[:, 0] == pname+'_ligand'].ix[:, 1:]
    ##compound=bind(pname,pname)
    ligands_n_neg = ligands_n_neg.append(ligand_n_neg, ignore_index = True)

ligand_neg = ligands_n_neg.ix[:, 1:]
protein_neg = proteins_neg.ix[:, 1:]
for i in range(proteins_neg.shape[0]):
    pname = proteins_neg.ix[i, 0]
    neg_list_used.append(pname)
compound_neg = DataFrame(np.hstack((protein_neg, ligand_neg)))
neg = neg.append(compound_neg, ignore_index = True)


print(compound_neg.shape)
#end = time()
#print((end - sta) / 60.0)


sta = time()
pos.to_hdf(mp_data+'/pos.h5', 'df')

pos_read = pd.read_hdf(mp_data+'/pos.h5', 'df')
pos_list_used = DataFrame(pos_list_used)
pos_list_used.to_csv(mp_data+'/pos_list.csv', index = False, header = ['name'])
pos_list_used.head()

end = time()
print((end - sta) / 60.0)

#########################
sta = time()
neg.to_hdf(mp_data+'/neg_clean.h5', 'df')

neg_read = pd.read_hdf(mp_data+'/neg_clean.h5', 'df')
neg_list_used = DataFrame(neg_list_used)
neg_list_used.to_csv(mp_data+'/neg_clean_list.csv', index = False, header = ['name'])
neg_list_used.head()

end = time()
print((end - sta) / 60.0)



##########################3










