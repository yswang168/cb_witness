#!/bin/bash

dirs=$1
# the directory
PY="python3.7 cb_witness.py"
first_witness()
{
for file in `ls ${dirs}/*.m`
do
 if [ ! -f $file-m ]; then
  if [ -s $file ]; then
    st="`grep ^UNSAT $file`"
  fi
  if [ ! -z "$st" ]; then
    continue
  fi
  line=`cat $file`
  line=${line/\[/}
  line=${line/\]/}
  line=${line/\n/}
  line=${line//,/}
  echo $line > $file-m
 fi
  Fcnf=${file/\.m/\.cnf}
  echo "$PY -t 7200 -v4 -TT_PYSAT -q $Fcnf $file-m"
  $PY -t 7200  -v4 -TT_PYSAT -q $Fcnf $file-m
done
}

second_witness()
{
for file in `ls ${dirs}/*.m-m`
do
  if [ -s $file ]; then
    st="`grep ^UNSAT $file`"
  fi
  if [ ! -z "$st" ]; then
    continue
  fi
  sed -i '/SAT/d' $file # remove the line which looks like "SATISFIABLE" 
  Fcnf=${file/\.m-m/\.cnf}
  Fwit=${file/\.m-m/\.wit}
  echo "$PY -t 7200 -v4 -TT_PYSAT -MUS_Solver=picomus -q $Fcnf $file"
  $PY -t 7200  -v4 -TT_PYSAT  -MUS_Solver=picomus -q $Fcnf $file 
done
}

#first_witness
second_witness

