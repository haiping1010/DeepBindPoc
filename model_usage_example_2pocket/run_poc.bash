for name in ????_w.pdb
do

base=${name%.pdb}
cd $base'_out'


python ../extract.py  $base


cd ..


done
