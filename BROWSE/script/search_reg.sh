#!/bin/bash
name=$1

media_path="/home/bba753951/Django/master_project/media/uploadfile"
ori_file=${media_path}"/original.csv"
tablefile=${media_path}"/table.csv"

head -n 1 $ori_file > $tablefile
grep ",${name}," $ori_file >> $tablefile

