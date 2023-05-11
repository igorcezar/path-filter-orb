#!/bin/sh

# If branch is specified, get files from there
if  [ "$BRANCH" != "" ]; then
    echo "Getting files from branch $BRANCH"
    git checkout "origin/$BRANCH"
fi

echo "Packing config..."
circleci config pack "$CONFIG_SOURCE" > "$CONFIG_OUTPUT"

echo "Validating config..."
circleci config validate "$CONFIG_OUTPUT"