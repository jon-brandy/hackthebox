#!/bin/bash

ZIPFILE=$1
RESULT=0

while [ $RESULT -eq 0 ]
do
PASSWORD=$( unzip -l $ZIPFILE | grep -E "^\s+[0-9]+" | grep -Eo "[0-9]+\.zip" | grep -Eo "[0-9]+" )
unzip -P "$PASSWORD" "$ZIPFILE"
RESULT=$?
ZIPFILE="$PASSWORD.zip"
done
