#!/bin/awk -f

BEGIN {
	OFS=","
    btn=0
}
{
    if (substr($0,1,1 )== "@" && btn == 0){

        btn =1
    }else if(btn ==1){
        btn = 0
        print $0 
    }

}
