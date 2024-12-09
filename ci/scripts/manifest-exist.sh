#!/bin/bash 

for dir in */; do
    count=$(find "$dir" -maxdepth 1 -type f \( -name "*-release.yaml" -o -name "*-release.yml" \) | wc -l);
    if [[ $count -ne 1 ]]; then
        echo "Directory '$dir' does not contain exactly one -release.yaml or -release.yml file.";
        exit 1;
    fi;
done;

echo "Checking for duplicates mainfest files..."

SEARCH_DIR=${1:-.}
TEMP_FILE="temp_release_files.txt"

find "$SEARCH_DIR" -type f \( -name "*-release.yaml" -o -name "*-release.yml" \) > "$TEMP_FILE"

if [[ -s $TEMP_FILE ]]; then
    DUPLICATES=$(sort "$TEMP_FILE" | uniq -d)
    if [[ -n "$DUPLICATES" ]]; then
        echo "Error: Duplicate files found:"
        echo "$DUPLICATES"
        rm -f "$TEMP_FILE"
        exit 1
    else
        echo "No duplicates found."
    fi
    else
    echo "No release files found in $SEARCH_DIR."
    exit 1
fi

rm -f "$TEMP_FILE"