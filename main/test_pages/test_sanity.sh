#!/bin/sh
for key in $(jq keys ./asd.json)
do
	pkey=$(echo $key | tr -d ','| tr -d ' ' | tr -d ']' | tr -d '[') 
	value=$(jq .[$pkey] asd.json)
	#echo  $pkey
	file=$(echo $pkey | tr -d "\"" | tr -d '\n')
	
	if (( $(echo $file | wc -m) > 12 ))
	then
		echo -e $file
		wget -qO- $value | diff $file -   || { echo FAILED $value; exit 1; }
	fi
done
