#!/bin/bash
correct=0
incorrect=0
for FILE in tests_out/*; 
do  
	if diff -w "${FILE}" "${FILE//tests_out/testout}" ; 
	then 
		echo $FILE PASSED ; 
		((correct+=1)) ; 
	else 
		echo $FILE FAILED; 
		((incorrect+=1)) ;  
	fi ; 
done

echo ""
echo "Test cases passed: $correct"

echo "Test cases failed: $incorrect"
