#!/bin/bash

function execute_git_command() {
    COMMAND=$1
    eval "${COMMAND}"
    COMMAND_EXIT_STATUS=$?

    if [ ${COMMAND_EXIT_STATUS} -ne 0 ]; then
        echo "Failed to execute: '${COMMAND}'"
        exit ${COMMAND_EXIT_STATUS}
    else
        echo "Successfully executed: '${COMMAND}'"
    fi
}

# The variable for the file to be resolved
FILENAME=<filename>

# Checkout to the PR's branch
execute_git_command "git checkout pull/18"

# Fetch the latest changes from the origin
execute_git_command "git fetch origin"

# Merge the main branch into the checked out branch
execute_git_command "git merge main"

# Fix the conflicts manually and then execute the following commands

# Add the file with resolved conflicts
execute_git_command "git add ${FILENAME}"

# Commit the changes with a proper message
execute_git_command 'git commit -m "Resolved conflicts in pull request #18"'

# Push the changes to the remote branch associated with PR #18
execute_git_command "git push origin pull/18"

# Please replace <filename> with actual file name