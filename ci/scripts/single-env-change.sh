#!/bin/bash 

# Get the list of changed files in the merge request
CHANGED_FILES=$(git diff --name-only origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...$CI_COMMIT_SHA)

# Filter the changes to files within the release folder
ENV_FOLDERS=$(echo "$CHANGED_FILES" | grep '^release/' | cut -d'/' -f2 | sort -u)

# Count the unique environment folders affected
ENV_COUNT=$(echo "$ENV_FOLDERS" | wc -l)

# Check if changes are made to only one environment folder
if [[ $ENV_COUNT -ne 1 ]]; then
    echo "Error: Changes must be restricted to a single environment folder.";
    echo "Affected environment folders: $ENV_FOLDERS";
    exit 1;
fi

# Print success message
echo "Validation passed: Changes are restricted to a single environment folder ($ENV_FOLDERS)."