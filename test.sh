#!/bin/bash

URL="https://42.fr"
DEPTH=1
PATH_DIR="42data"

if [ ! -f "spider.py" ]; then
    echo "Error: spider.py not found in the current directory."
    exit 1
fi

mkdir -p "$PATH_DIR"

python3 spider.py "$URL" -l "$DEPTH" -p "$PATH_DIR" -r