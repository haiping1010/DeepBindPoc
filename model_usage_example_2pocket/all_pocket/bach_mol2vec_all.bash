source activate my-rdkit-env
for name in  {7..9}*.mol2

do
base=${name%_ligand.mol2}

nohup bash part1.bash $base    &
echo $name
sleep 0.2s

done

