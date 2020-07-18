#!/bin/bash

shell_folder=$(cd "$(dirname "$0")";pwd)
. ${shell_folder}/framefunction.sh
. ${shell_folder}/filefunction.sh

step6_path=$1
way=$2
step6_file=${step6_path}${way}"/step6_transcript_regulator.csv"
gene_file=${step6_path}"gene_file.csv"




checkFile $step6_file
checkFile $gene_file
checkNewline $step6_file
checkNewline $gene_file

find_col transcript_name $step6_file
step6_tran_col=$?


find_col transcript_name $gene_file
gene_tran_col=$?
find_col Gene_name $gene_file
gene_col=$?

join -t, -a 2 -e 0 -o 1.${gene_col},2.1,2.2,2.3\
    <(sed '1d' $gene_file|LC_ALL=C sort -t, -k ${gene_tran_col},${gene_tran_col} )\
    <(sed '1d' $step6_file |LC_ALL=C sort -t, -k ${step6_tran_col},${step6_tran_col} )\
    | sed '1i Gene_name,transcript_name,regulator_sum,regulator_name'\
    > ${step6_path}"temp.csv"


jq -s -R -c -f ${shell_folder}/csv2json.jq ${step6_path}"temp.csv" > ${step6_path}${way}"/step6_transcript_regulator.json"
