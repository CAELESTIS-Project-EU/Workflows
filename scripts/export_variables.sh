#!/bin/bash

# Check if at least one key-value pair is provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 key1=value1 key2=value2 ..."
    exit 1
fi

# Loop through provided key-value pairs and export them
for var in "$@"; do
    export "$var"
    echo "Exported: $var"
done

echo "Export completed."
