#!/bin/bash

# Check if at least one key-value pair is provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 key1=value1 key2=value2 ..."
    exit 1
fi

for arg in "$@"; do
    IFS='=' read -r key value <<< "$arg"
    export "$key"="$value"
    echo "Exported: $key=$value"
done


echo "Export completed."
