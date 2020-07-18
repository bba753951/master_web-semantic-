inp=$1
oup_path=$2

#start from 2 bcz column name
#end to < NF bcz , at the end
head -n 1 $inp|awk -F, '{for(i=2;i<NF;i++)print $i}' >$oup_path"/transcript_name"
tail -n 1 $inp|awk -F, '{for(i=2;i<NF;i++)print $i}' >$oup_path"/regulator_name"
