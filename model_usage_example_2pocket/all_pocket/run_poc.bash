source activate my-rdkit-env


for name in      ????_w_pocket_n*.pdb
do


nohup python  test_poc.py $name &
sleep 1s



done
