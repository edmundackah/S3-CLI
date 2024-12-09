#!/bin/bash

# Colors for output
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RESET="\033[0m"

echo -e "${YELLOW}Starting validation of maintenance flags...${RESET}"

# Check for maintenance-flags.yml or maintenance-flags-aws.yml at the root of the release folder
ROOT_FILE_COUNT=$(find release -maxdepth 1 -type f \( -name "maintenance-flags.yml" -o -name "maintenance-flags-aws.yml" \) | wc -l)
if [[ $ROOT_FILE_COUNT -ne 0 ]]; then
  echo -e "${RED}Error: The release folder must not contain maintenance-flags.yml or maintenance-flags-aws.yml files at its root.${RESET}"
  exit 1
fi

# Find all environment folders in the release folder
ENV_FOLDERS=$(find release -mindepth 1 -maxdepth 1 -type d)

VALIDATION_STATUS=0

# Check each environment folder
for ENV in $ENV_FOLDERS; do
  # Count maintenance-flags.yml at the root of the environment folder
  FLAGS_FILE_COUNT=$(find "$ENV" -maxdepth 1 -type f -name "maintenance-flags.yml" | wc -l)

  # Count maintenance-flags-aws.yml at the root of the environment folder
  AWS_FLAGS_FILE_COUNT=$(find "$ENV" -maxdepth 1 -type f -name "maintenance-flags-aws.yml" | wc -l)

  # Check if the maintenance-flags.yml file is missing or duplicated
  if [[ $FLAGS_FILE_COUNT -ne 1 ]]; then
    echo -e "${RED}Error: $ENV must have exactly one maintenance-flags.yml file at its root, found $FLAGS_FILE_COUNT.${RESET}"
    VALIDATION_STATUS=1
  fi

  # Check if the maintenance-flags-aws.yml file is missing or duplicated
  if [[ $AWS_FLAGS_FILE_COUNT -ne 1 ]]; then
    echo -e "${RED}Error: $ENV must have exactly one maintenance-flags-aws.yml file at its root, found $AWS_FLAGS_FILE_COUNT.${RESET}"
    VALIDATION_STATUS=1
  fi

  # Ensure maintenance-flags.yml does not exist elsewhere in the folder
  EXTRA_FLAGS_COUNT=$(find "$ENV" -mindepth 2 -type f -name "maintenance-flags.yml" | wc -l)
  if [[ $EXTRA_FLAGS_COUNT -ne 0 ]]; then
    echo -e "${RED}Error: $ENV contains maintenance-flags.yml files outside its root.${RESET}"
    VALIDATION_STATUS=1
  fi

  # Ensure maintenance-flags-aws.yml does not exist elsewhere in the folder
  EXTRA_AWS_FLAGS_COUNT=$(find "$ENV" -mindepth 2 -type f -name "maintenance-flags-aws.yml" | wc -l)
  if [[ $EXTRA_AWS_FLAGS_COUNT -ne 0 ]]; then
    echo -e "${RED}Error: $ENV contains maintenance-flags-aws.yml files outside its root.${RESET}"
    VALIDATION_STATUS=1
  fi
done

# Final validation result
if [[ $VALIDATION_STATUS -eq 0 ]]; then
  echo -e "${GREEN}Validation passed: All environment folders contain one and only one maintenance-flags.yml and maintenance-flags-aws.yml at their root.${RESET}"
  exit 0
else
  echo -e "${RED}Validation failed. Please fix the issues above.${RESET}"
  exit 1
fi