#!/bin/sh
$URIS=./uris.json 
for key in $(jq keys $URIS)
do
	pkey=$(echo $key | tr -d ','| tr -d ' ' | tr -d ']' | tr -d '[') 
	value=$(jq .[$pkey] $URIS)
	file=$(echo $pkey | tr -d "\"" | tr -d '\n')
	
	if (( $(echo $file | wc -m) > 12 ))
	then
		echo -e $file
		wget -qO- $value | diff $file -
	fi
    # on fail either save the new file or exit
	retVal=$?
	if [ $retVal -ne 0 ]; then
		if [ $1 == "--sync" ]; then
			wget $value -O $file
		else
			echo FAILED $value; 
			exit 1; 
		fi
	fi
done
