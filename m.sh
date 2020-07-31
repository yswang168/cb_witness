#! /bin/bash

declare -a ds
declare -a sl
sl=("cadical" "minimal" "clingo" "dlv")
ds=(200) #50 100 150)
for i in ${ds[@]}
do
	for j in 0 # 1 2
	do
		(time python3 data/run.py $i $i $j) &>> ${sl[$j]}.txt
	done
done
