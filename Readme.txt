
1. the fpocket was used to generate the decoy pocket of protein PDB (bash  run_all.bash;bash run_poc.bash) (befor do the pocket extract make sure the PDB is without ligand and water, only contain protein atoms)
2. the ligand and pocket are converted into vector by mol2vec (cd all_known_pocket/;bash bach_mol2vec.bash ; bash run_poc_vec.bash; cd ../)



3. the vector of ligand and pocket are concatnated into one vector. And saved into file mp_data/pos.h5. (mkdir mp_data; python data_process_all_test.py all_known_pocket  mp_data).  The all_known_pocket is the place where your ligand vector file; The mp_data is where your output folder.

4. the deep_dense_FC_load_n.py  script was used to load the model and do the prediction.


other script that may help:
run_x.bash (clean the protein PDB)
run_all_ligand.bash  (extract ligand )
cd all_known_pocket/;bash run_poc_extract.bash   (extract known pocket based on ligand)

