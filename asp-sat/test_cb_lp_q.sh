#!/bin/bash

dirs=$1

# the directory
PY="python3.7 cb_witness.py"

for file in `ls ${dirs}/*.m` #cat ${dirs}/SAT`
do
#  if [ -e ${file/.m/\.wit} ]; then
#    continue
#  fi
  Mlp=$file #${dirs}"/"${file}
  RES="`grep UNSAT $Mlp`"
  if [ ! -z $RES ]; then
    continue
  fi
  RES="`grep UNKNOWN $Mlp`"
  if [ ! -z $RES ]; then
    continue
  fi
  Flp=${Mlp/\.m/\.lp}
  echo "$PY -t 7200 -lp -v4 -TT_PYSAT -q -MUS_Solver=picomus $Flp $Mlp"
  # $PY -t 7200 -lp -v4 -TT_PYSAT -q $Flp $Mlp
  $PY -t 7200 -lp -v4 -TT_PYSAT -q -MUS_Solver=picomus $Flp $Mlp 
done
