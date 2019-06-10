import sys
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.Chem import PandasTools
###from rdkit.Chem.Draw import IPythonConsole
##import matplotlib.pyplot as plt
##import seaborn as sns
from mol2vec.features import mol2alt_sentence, MolSentence, DfVec, sentences2vec
##from mol2vec.helpers import depict_identifier, plot_2D_vectors, IdentifierTable, mol_to_svg

aa_smis = ['CC(N)C(=O)O', 'N=C(N)NCCCC(N)C(=O)O', 'NC(=O)CC(N)C(=O)O', 'NC(CC(=O)O)C(=O)O',
          'NC(CS)C(=O)O', 'NC(CCC(=O)O)C(=O)O', 'NC(=O)CCC(N)C(=O)O', 'NCC(=O)O',
          'NC(Cc1cnc[nH]1)C(=O)O', 'CCC(C)C(N)C(=O)O', 'CC(C)CC(N)C(=O)O', 'NCCCCC(N)C(=O)O',
          'CSCCC(N)C(=O)O', 'NC(Cc1ccccc1)C(=O)O', 'O=C(O)C1CCCN1', 'NC(CO)C(=O)O',
          'CC(O)C(N)C(=O)O', 'NC(Cc1c[nH]c2ccccc12)C(=O)O', 'NC(Cc1ccc(O)cc1)C(=O)O',
          'CC(C)C(N)C(=O)O']
aa_codes = ['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLU', 'GLN', 'GLY', 'HIS', 'ILE', 
            'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL']

aas = [Chem.MolFromSmiles(x) for x in aa_smis]

from gensim.models import word2vec
model = word2vec.Word2Vec.load('/share/home/zhanghaiping/program/mol2vec/examples/models/model_300dim.pkl')
aa_sentences = [mol2alt_sentence(x, 1) for x in aas]
aalist={}
index=0
for x in aa_sentences:

    aa= np.zeros(300)
    for y in x:
        aa=aa+model.wv.word_vec(y)
    aalist[aa_codes[index]]=aa
    #print (aa)
    index=index+1


for name in aa_codes:
    print (name,  aalist[name] )
    #print (name, ' '.join( str(x) for x in list[name]))





if len(sys.argv) <1 :
   print("python python2_L.py xxx")
filebase=sys.argv[1]
##filebase=file.replace(".pdb","")
print(filebase)
pocVec= np.zeros(300)
for line in open(filebase):
    tem_B=' '
    if len(line)>16:
       tem_B=line[16]
       line=line[:16]+' '+line[17:]
    #print(line)
    list = line.split()
    id = list[0]
    #pocVec= np.zeros(300)
    if id == 'ATOM' and tem_B !='B':
        type = list[2]
        if type == 'CA' and list[3]!= 'UNK':
            residue = list[3]
            type_of_chain = line[21:22]
            print (residue)
            pocVec=pocVec+aalist[residue]

foo = open(filebase + "_pocVec.txt", "w")
foo.write(str(pocVec))



