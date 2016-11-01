#! /bin/bash -u

filename=$1

while read file
do
   solve-field --ra 330.896 --dec 18.914 --radius 0.35 ${file}  # complete this line with your call to solve-field
done < ${filename}
