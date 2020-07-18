#!/bin/bash
name=$1
file_path=$2
infile=$3
outfile=$4

in=${file_path}${infile}
out=${file_path}${outfile}

head -n 1 $in > $out
grep ",${name}," $in >> $out


#jq -s -R -c -f ${shell_folder}/csv2json.jq ${step6_path}"/temp.csv" > ${step6_path}"/step6_transcript_regulator.json"
