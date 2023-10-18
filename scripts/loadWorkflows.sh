#!/bin/bash

# Check if the correct number of arguments are provided
if [[ $# -ne 3 ]]; then
    echo "Usage: ./loadWorkflow.sh <destination_path> <workflow_name> <machinee>"
    exit 1
fi

# Assign arguments to variables
DEST_PATH="$1"
WORKFLOW="$2"
MACHINE="$3"

# Create the BACKEND directory in the destination path
mkdir -p "$DEST_PATH/BACKEND"

# Copy the PHASES folder to the destination path
cp -r /gpfs/projects/bsce81/alya/tests/workflow_stable/PHASES "$DEST_PATH"

# Copy the api.py  and init files to the BACKEND directory in the destination path
cp /gpfs/projects/bsce81/alya/tests/workflow_stable/BACKEND/api.py "$DEST_PATH/BACKEND/"
cp /gpfs/projects/bsce81/alya/tests/workflow_stable/BACKEND/__init__.py "$DEST_PATH/BACKEND/"

# Copy the specified workflow to the BACKEND directory in the destination path
cp -r "/gpfs/projects/bsce81/alya/tests/workflow_stable/BACKEND/$WORKFLOW" "$DEST_PATH/BACKEND/"

# Copy the specified workflow to the SCRIPTS directory in the destination path
cp -r "/gpfs/projects/bsce81/alya/tests/workflow_stable/scripts/" "$DEST_PATH"

# Check if the operations were successful
if [[ $? -eq 0 ]]; then
    echo "Files and folders copied successfully"
else
    echo "Error occurred while copying."
fi

#chmod +x "$DEST_PATH/BACKEND/$WORKFLOW/load-workflow.sh"
# shellcheck disable=SC1090
# source $DEST_PATH/BACKEND/$WORKFLOW/load-workflow.sh $DEST_PATH

# Assuming DEST_PATH contains the path with or without a trailing slash
if [[ $DEST_PATH == */ ]]; then
    DEST_PATH="${DEST_PATH%/}"
fi

chmod +x "$DEST_PATH/scripts/mn/loadModule.sh"
chmod +x "$DEST_PATH/scripts/nord/loadModule.sh"
# shellcheck disable=SC1090
source $DEST_PATH/scripts/$MACHINE/loadModule.sh $DEST_PATH