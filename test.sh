#!/usr/bin/env bash

# ANSI color codes
RED="\033[31m"
GREEN="\033[32m"
RESET="\033[0m"

# Function to run a test and handle failures
run_test() {
    local message="$1"
    local input="$2"
    local expected="$3"
    local ERROR_CODE

    echo -e "${GREEN}$message${RESET}"
    sleep 1  # Optional sleep for better output organization

    venv/bin/python -c "from app import get_label; assert get_label('$input') == '$expected'"

    ERROR_CODE=$?

    if [ ${ERROR_CODE} != 0 ]; then
        echo -e "${RED}Test '$message' failed.${RESET}"
    else
        echo -e "${GREEN}Test '$message' succeeded.${RESET}"
    fi
}

echo -e "${GREEN}Start integration test${RESET}"

echo -e "${GREEN}Pull required images${RESET}"
docker compose pull

echo -e "${GREEN}Run Weaviate and Contextuary docker containers${RESET}"
docker compose up -d

echo -e "${GREEN}Wait for the service to spin up${RESET}"
sleep 5

# Run both tests, regardless of the outcome of the first test
run_test "Test 1: 'you are awesome' is not toxic" "you are awesome" "Non Toxic"
run_test "Test 2: 'you are an idiot' is toxic" "you are an idiot" "Toxic"

echo "All tests executed"
docker compose down




