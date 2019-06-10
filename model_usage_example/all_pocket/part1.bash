#source activate my-rdkit-env

name=$1

babel -imol2  $name'_ligand.mol2' -osmi   $name'_ligand.smi'
mol2vec featurize -i   $name'_ligand.smi' -o    $name'.csv' -m     /share/home/zhanghaiping/program/mol2vec/examples/models/model_300dim.pkl   --uncommon UNK -r 1

