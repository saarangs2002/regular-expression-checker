#!/bin/bash
correct=0
incorrect=0

mkdir -p tests_out

for FILE in tests/*; 
do  

	python3 project.py < $FILE > "${FILE//tests/tests_out}";
		
	if diff -w "${FILE//tests/tests_out}" "${FILE//tests/tests_expected}" ; 
	then 
		echo $FILE PASSED ; 
		((correct+=1)) ; 
	else 
		echo $FILE FAILED; 
		((incorrect+=1)) ;  
	fi ; 
	echo "-------------------------------"
done

echo ""
echo "Test cases passed: $correct"

echo "Test cases failed: $incorrect"
