source activate my-rdkit-env
for name in  *_ligand_n.mol2

do
base=${name%.mol2}
babel -imol2   $name  -osmi $base'.smi'
mol2vec featurize -i $base'.smi' -o  $base'.csv' -m   model_300dim.pkl  --uncommon UNK -r 1
echo $name
done

