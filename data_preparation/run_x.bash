for name in ????.pdb
do
base=${name%.pdb}
grep  -r "ATOM\|TER\|END" $name > $base'_w.pdb'

done
