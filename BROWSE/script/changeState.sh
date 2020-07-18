id=$1
old_state=$2
new_state=$3
info_path='/home/bba753951/Django/master_project/media/info/'
media_path='/home/bba753951/Django/master_project/media/uploadfile/'
info_file=info.csv
line_num=$(grep -m1 -n -P "^"$id ${info_path}${info_file}|head -n1|cut -d: -f 1)

if [ "$line_num" == "" ];then
    echo "cani\'t find the $id in info.csv"
    exit 1
fi

sed -i "$line_num s/,${old_state}$/,${new_state}/" ${info_path}${info_file}

echo ==============change state==================
echo $id from $old_state to $new_state

