#!/bin/bash

# Check if the correct number of arguments are provided
if [[ $# -ne 2 ]]; then
    echo "Usage: ./loadWorkflow.sh <destination_path> <machine>"
    exit 1
fi

# Assign arguments to variables
DEST_PATH="$1"
MACHINE="$2"


# Assuming DEST_PATH contains the path with or without a trailing slash
if [[ $DEST_PATH == */ ]]; then
    DEST_PATH="${DEST_PATH%/}"
fi

chmod +x "$DEST_PATH/scripts/mn/loadModule.sh"
chmod +x "$DEST_PATH/scripts/nord/loadModule.sh"
# shellcheck disable=SC1090
source $DEST_PATH/scripts/$MACHINE/loadModule.sh $DEST_PATH
