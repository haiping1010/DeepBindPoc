

babel  -ipdb   6QTN_ACP_ligands_n.pdb  -omol2  6QTN_ACP_ligand_n.mol2

python   extract_pocket.py     6QTN   6QTN_ACP_ligand_n.mol2


mv 6QTN_poc.pdb  6QTN_ACP_poc.pdb

babel  -ipdb   6QTN_GTP_ligands_n.pdb  -omol2  6QTN_GTP_ligand_n.mol2

python   extract_pocket.py     6QTN   6QTN_GTP_ligand_n.mol2

mv 6QTN_poc.pdb  6QTN_GTP_poc.pdb

