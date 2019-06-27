cat  ligand_select_f.txt  | while read line  
do

IFS=' ' read -r -a array <<< $line
base=${array[0]%.pdb}

#echo ${#array[@]}
if [ ${#array[@]} == 3 ]; then
   grep  -r    ${array[1]}   $base'_ligands.pdb' >tem.pdb
   grep -r " ${array[2]} "   tem.pdb  > $base'_'${array[1]}'_ligands_n.pdb'

   grep  "^TER\|^END\|^ATOM"   $base'.pdb'| grep  " ${array[2]} "  > $base'_'${array[1]}'_w.pdb'
 
   echo ${array[2]}
   echo $base'_w.pdb'

fi

if [  ${#array[@]} == 2 ]; then
   grep  -r    $array[1]   $base'_ligands.pdb'   > $base'_ligands_n.pdb'

fi


#mv $base*  move/
done
