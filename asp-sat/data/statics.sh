#! /bin/bash

# statics the average time, memory and clauses with more than two positive literals in the derivation

# usage
# $0 FILE

tc=0
mc=0
ac=0
grep clauses $1 | cut -f 1 -d" " > /tmp/$$

while read nc 
do
  let ac=$ac+$nc
done <  /tmp/$$ 

grep Time $1 | cut -f 2 -d" " > /tmp/$$.t
while read time
do
  tc=`echo "scale=4; $tc+$time"|bc`
done </tmp/$$.t

grep Memory $1 | cut -f 2 -d " " > /tmp/$$.m
while read mem
do
  mc=`echo "scale=4; $mc+$mem"|bc`
done </tmp/$$.m

num=`wc -l /tmp/$$ | cut -f 1 -d" "`
tc=`echo "scale=2; $tc/$num"|bc`
mc=`echo "scale=2; $mc/$num"|bc`
ac=`echo "scale=2; $ac/$num"|bc`

echo 'A-time(s) A-memory(M) A-clauses'
echo $tc $mc $ac

rm -fr /tmp/$$.*
