info_path='/home/bba753951/Django/master_project/media/info/'
media_path='/home/bba753951/Django/master_project/media/uploadfile/'

# find state=1
info=$(grep -m1 -n -P ",1$" ${info_path}info.csv|head -n1)
# find state=2
running=$(grep -m1 -n -P ",2$" ${info_path}info.csv|head -n1)


# for id name of state = 1
id=$(echo $info|cut -d: -f 2|cut -d, -f 1)


echo $id

if [ "$running" != "" ];then
    echo Already has a running task 
    exit 1
fi

if [ "$id" == "" ];then
    echo no ready task
    exit 1
fi



nohup bash ${media_path}${id}"/run.sh" > ${media_path}${id}"/run.out" &

