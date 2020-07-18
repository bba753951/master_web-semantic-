file=$1
file_path=$(dirname $file)
echo $file_path
list=$(unzip -l $file)

name1="read.fastq"
name2="targetRNA.fasta"
name3="regulator.fasta"
name4="gene_file.csv"

function checkfile(){
    local fileInfo=$1
    local filename=$2
    echo "$fileInfo"|grep -q $filename
    local result=$?
    if [ $result -eq 1 ];then
        echo $filename not exists 
        exit 1
    fi

}

checkfile "$list" $name1
checkfile "$list" $name2
checkfile "$list" $name3


echo ==============unzip file==================
unzip -d $file_path $file


hyb_path=$(find $file_path -name $name1)
tran_path=$(find $file_path -name $name2)
reg_path=$(find $file_path -name $name3)
gene_path=$(find $file_path -name $name4)

echo $hyb_path
echo $tran_path
echo $reg_path
echo $gene_path

mv $hyb_path $file_path/hyb_file.fastq
mv $tran_path $file_path/tran_file.fasta
mv $reg_path $file_path/reg_file.fasta

if [ "$gene_path" != "" ];then
    mv $gene_path $file_path
fi




