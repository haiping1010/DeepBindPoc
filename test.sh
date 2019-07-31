#!/bin/sh
####################  bash test.sh  xxx  jobxxx   ###############

CHANGEDIR=`pwd`

prot=$1
ligand=$1
path=$2

echo $path
echo $prot

#################generate pocket###########
cd $path
rm -rf  *.csv
grep  -r "ATOM\|TER\|END" $prot'_protein.pdb' > $prot'_protein_w.pdb'

fpocket -f  $prot'_protein_w.pdb'

cd $prot'_protein_w_out'

python $CHANGEDIR/data_preparation/extract.py  $prot'_protein_w'
mkdir ../all_pocket
cp -r $prot'_protein_w_pocket_n'*.pdb  ../all_pocket

cd ../all_pocket

#################convert pocket and ligand to vector######
source activate my-rdkit-env

for name in     $prot'_protein_w_pocket_n'*.pdb
do
nohup python  $CHANGEDIR/data_preparation/test_poc.py  $CHANGEDIR  $name &
sleep 2s
done

cd ../

conda deactivate
babel -ipdb   $ligand'_ligand.pdb'  -osmi $ligand'_ligand.smi'
source activate my-rdkit-env

mol2vec featurize -i  $ligand'_ligand.smi'  -o  $ligand'_ligand.csv' -m  $CHANGEDIR/model/model_300dim.pkl  --uncommon UNK -r 1

#################combine the pocket and ligand into one file#######
conda deactivate

mkdir mp_data
python $CHANGEDIR/data_preparation/data_process_all_test.py   .  mp_data



#################do the prediction##############

python  $CHANGEDIR/load_model_script/deep_dense_FC_load_n.py   $CHANGEDIR'/model'


mkdir  DeepBindPoc_output
cp -r  out_list.csv   all_pocket/*.pdb   DeepBindPoc_output

zip -q -r  $prot'_result.zip'  DeepBindPoc_output
#################finished#####################


    
    
    
    
    
