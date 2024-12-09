#!/bin/bash

# Colors for output
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RESET="\033[0m"

# Output files
MAINTENANCE_FILE="modified_maintenance_files.txt"
RELEASE_FILE="spa-releases.txt"

echo -e "${YELLOW}Checking for modified maintenance files and release files in the current commit...${RESET}"

# Get the list of modified and renamed files (exclude deleted) for maintenance files
MODIFIED_MAINTENANCE_FILES=$(git diff --name-only --diff-filter=AM "HEAD^" "$CI_COMMIT_SHA" -- \
  '*maintenance-flags.yml' \
  '*maintenance-flags.yaml' \
  '*maintenance-flags-aws.yml' \
  '*maintenance-flags-aws.yaml')

# Get the list of modified and renamed files (exclude deleted) for release files
MODIFIED_RELEASE_FILES=$(git diff --name-only --diff-filter=AM "HEAD^" "$CI_COMMIT_SHA" -- \
  '*-release.yml' \
  '*-release.yaml')

# Process modified maintenance files
if [[ -z "$MODIFIED_MAINTENANCE_FILES" ]]; then
  echo -e "${GREEN}No modified maintenance files found.${RESET}"
else
  # Remove duplicates and save to file
  echo "$MODIFIED_MAINTENANCE_FILES" | sort | uniq > "$MAINTENANCE_FILE"
  echo -e "${GREEN}Modified maintenance files have been saved to '$MAINTENANCE_FILE':${RESET}"
  cat "$MAINTENANCE_FILE"
fi

# Process modified release files
if [[ -z "$MODIFIED_RELEASE_FILES" ]]; then
  echo -e "${GREEN}No modified release files found.${RESET}"
else
  # Remove duplicates and save to file
  echo "$MODIFIED_RELEASE_FILES" | sort | uniq > "$RELEASE_FILE"
  echo -e "${GREEN}Modified release files have been saved to '$RELEASE_FILE':${RESET}"
  cat "$RELEASE_FILE"
fi