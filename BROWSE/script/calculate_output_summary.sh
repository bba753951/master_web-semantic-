file_path=$1
way=$2

hybrid_file=hyb_file.fastq
trimmed_hybrid_file=hyb_file_clipped_qf.fastq
uniq_trimmed_hybrid_file=hyb_file_step1.csv
result_hybrid_file=step6_hybrid_transcript.csv
result_pair_file=step6.csv


declare -i hybrid_count=$(expr $(wc -l ${file_path}${hybrid_file}|cut -d" " -f 1) / 4)
declare -i trimmed_hybrid_count=$(expr $(wc -l ${file_path}${trimmed_hybrid_file}|cut -d" " -f 1) / 4)
declare -i uniq_trimmed_hybrid_count=$(wc -l ${file_path}${uniq_trimmed_hybrid_file}|cut -d" " -f 1)
declare -i result_hybrid_count=$(wc -l ${file_path}${way}/${result_hybrid_file} |cut -d" " -f 1)
declare -i result_pair_count=$(wc -l ${file_path}${way}/${result_pair_file} |cut -d" " -f 1)

uniq_trimmed_hybrid_file=${uniq_trimmed_hybrid_file}-1
result_hybrid_count=${result_hybrid_count}-1
result_pair_count=${result_pair_count}-1

cent_uniq_trimmed=$(printf "%.2f" $(echo "scale=2;${uniq_trimmed_hybrid_count}*100/${hybrid_count}"|bc))
cent_trimmed=$(printf "%.2f" $(echo "scale=2;${trimmed_hybrid_count}*100/${hybrid_count}"|bc))
cent_result=$(printf "%.2f" $(echo "scale=2;${result_hybrid_count}*100/${hybrid_count}"|bc))




echo "$hybrid_count (100.00 %),$trimmed_hybrid_count ($cent_trimmed %),$uniq_trimmed_hybrid_count ($cent_uniq_trimmed %),$result_hybrid_count ($cent_result %), $result_pair_count" > ${file_path}${way}/output_summary.csv 
