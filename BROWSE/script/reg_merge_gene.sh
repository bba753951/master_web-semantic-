
shell_folder=$(cd "$(dirname "$0")";pwd)
. ${shell_folder}/framefunction.sh
. ${shell_folder}/filefunction.sh

infile=$1
gene_file=$2
outfile=$3




checkFile $infile
checkFile $gene_file
checkNewline $infile
checkNewline $gene_file

find_col transcript_name $infile
step6_tran_col=$?


find_col transcript_name $gene_file
gene_tran_col=$?
find_col Gene_name $gene_file
gene_col=$?

join -t, -1 $gene_tran_col -2 $step6_tran_col -e 0 -o 1.${gene_col},2.${step6_tran_col}\
    <(sed '1d' $gene_file|LC_ALL=C sort -t, -k ${gene_tran_col},${gene_tran_col} )\
    <(sed '1d' $infile |LC_ALL=C sort -t, -k ${step6_tran_col},${step6_tran_col} )\
    | sed '1i Gene_name,transcript_name'\
    > $outfile

