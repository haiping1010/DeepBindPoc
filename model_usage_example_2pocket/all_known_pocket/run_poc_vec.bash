source activate my-rdkit-env


for name in     ????_???_poc.pdb
do


nohup python  test_poc.py $name &
sleep 1s



done
