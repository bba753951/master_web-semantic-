#!/bin/jq -f

#jq -s -R -f pra.jq c.csv

# transform form csv to json for Databale
[                                               
	split("\n")[]                  
	|split(",")
	|select(length>0) 
]                                
	|{"data":.[1:],"column":[0]}
