#!/bin/bash
# Under pbaccs list all the accounts you need to check.
# The delimiter can be changed if you want to output this 
# to some other tool. 
pbaccs=(
"unix"
"linux"
"opsunix"
"opslinux"
"splunk"
"bob"
"nonbob"
)

delimiter=","
for i in "${pbaccs[@]}"
do
   getent passwd $i > /dev/null
   Status=$?
   if [[ "$Status" == 0  ]]; then
     #echo "$i" 
     results="$results$delimiter$i"
   fi
   # or do whatever with individual element of the array
done
echo $results
