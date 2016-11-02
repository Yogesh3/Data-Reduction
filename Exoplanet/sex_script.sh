#! /bin/bash -u

filelist=$1

while read -r file
do
    echo ${file} | sed 's|.txt|.cat|' > basename 
    sex ${file} -c default.sex -CATALOG_NAME ${basename}
done < ${filelist}
