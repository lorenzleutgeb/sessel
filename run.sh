#!/bin/bash

set -ex

for i in 1 2 3 4
do
	if [ ! -e ${i}.wav ]
	then
		echo ${i}.wav missing!
		read
		exit
	fi
done

python sessel.py 1.wav 2.wav 3.wav 4.wav
