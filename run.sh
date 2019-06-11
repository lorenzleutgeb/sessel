#!/bin/bash

set -ex

for i in 1 2 3 4
do
	if [ ! -e ${i}.ogg ]
	then
		echo ${i}.ogg missing!
		read
		exit
	fi
done

python sessel.py 1.ogg 2.ogg 3.ogg 4.ogg
