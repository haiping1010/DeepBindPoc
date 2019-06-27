#!/bin/sh
####################  bash test_batch.sh  yyy  jobs/jobyyy   ###############

CHANGEDIR="."

prot_ligands=$1

path=$2

echo $path
echo $prot

#################generate pocket###########
cd $path

unzip   -j  $prot_ligands'.zip' 


mkdir ../all_pocket
for name in ????.pdb
do
base=${name%.pdb}
grep  -r "ATOM\|TER\|END" $name  > $base'_protein_w.pdb'

fpocket -f  $base'_protein_w.pdb'

cd $base'_protein_w_out'

python $CHANGEDIR/data_preparation/extract.py  $base'_protein_w'
cp -r $base'_protein_w_pocket_n'*.pdb  ../all_pocket
cd ..

done

cd all_pocket



#################convert pocket and ligand to vector######
source activate my-rdkit-env

for name in     ????'_protein_w_pocket_n'*.pdb
do
nohup python  $CHANGEDIR/data_preparation/test_poc.py  $CHANGEDIR  $name &
sleep 2s
done

cd ../

#conda deactivate
for name in ????_ligand.pdb
do
base=${name%_ligand.pdb}
conda deactivate
babel -ipdb   $base'_ligand.pdb'  -osmi $base'_ligand.smi'
source activate my-rdkit-env

mol2vec featurize -i  $base'_ligand.smi'  -o  $base'_ligand.csv' -m  $CHANGEDIR/model/model_300dim.pkl  --uncommon UNK -r 1

done
#################combine the pocket and ligand into one file#######
conda deactivate

mkdir mp_data
python $CHANGEDIR/data_preparation/data_process_all.py   .  mp_data

#################do the prediction##############

python  $CHANGEDIR/load_model_script/deep_dense_FC_load_n.py   $CHANGEDIR'/model'

mkdir  DeepBindPoc_output
cp -r  out_list.csv   all_pocket/*.pdb   DeepBindPoc_output

zip -q -r  $prot'_result.zip'  DeepBindPoc_output
#################finished#####################


    
    
    
    
    
