#!/bin/bash

# check number of args
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# check if GeneratedFiles exists
if [ ! -d "GeneratedFiles" ]; then
    mkdir GeneratedFiles
fi

# get filename from args
filename="$1"
base=$(basename "$filename")
base_without_ext="${base%.*}"

# Run script
uic -o "GeneratedFiles/ui_$base_without_ext.h" "$filename" 

if [ $? -ne 0 ]; then
    echo "Error: uic failed"
    exit 1
fi

echo "ui_$base_without_ext.h successfully created"

# edit pro file and generate .cpp and .h
python3 editPro.py "$base_without_ext"