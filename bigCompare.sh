#!/bin/bash
#This script loads, into a mysql table, lines of txt files generated by clean_logs.sh

# Browse all directories of inputQueries and liftDeductions to compare them by calling the filesCompare.py script

# for d in */; do

# find inputQueries -d 1 -type d -name "*" -print
dirsIn=($(find data/inputQueries -d 1 -type d))
dirsOut=($(find data/liftDeductions/deducedBGPs -d 1 -type d))
for din in "${dirsIn[@]}"; do
	for dout in "${dirsOut[@]}"; do
		if [ $(basename $din) == $(basename $dout) ]
		then
     		echo "$din"
    		echo "$dout"
 			python3.6 filesCompare.py "$din" "$dout"
    	fi
    done
done