#!/bin/bash

DATA_DIR="$(pwd)/data/5104873/applications"
OUTPUT_DIR="$(pwd)/data/uspto_json/applications"

# iterate through all xml files in the data directory
for file in $DATA_DIR/**/*.xml; do
    # get the filename without the extension
    filename=$(basename -- "$file")
    filename="${filename%.*}"
    # convert the xml file to json
    cat $file | xq . > $OUTPUT_DIR/$filename.json
done
