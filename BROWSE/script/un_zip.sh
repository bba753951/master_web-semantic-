echo ========= SH:unzip ===========

file_path=$1
echo $file_path
unzip -jp $file_path"read.zip" > $file_path"hyb_file.fastq"
unzip -jp $file_path"target.zip" > $file_path"tran_file.fasta"
unzip -jp $file_path"regulator.zip" > $file_path"reg_file.fasta"
#echo unzip -jp $file_path"regulator.zip"  $file_path"reg_file.fasta"
