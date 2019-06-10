for name in ????_w.pdb
do

base=${name%_w.pdb}

#5OVE_ligands_n.pdb
babel  -ipdb   $base'_ligands_n.pdb'  -omol2  $base'_ligand_n.mol2'

python   extract_pocket.py    $base


done
