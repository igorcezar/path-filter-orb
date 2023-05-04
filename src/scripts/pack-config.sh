#!/bin/bash

if  [ "$BRANCH" != "$CIRCLE_BRANCH" ]; then
    git checkout "$BRANCH" "$CONFIG_SOURCE"
fi

echo "Packing config..."
circleci config pack "$CONFIG_SOURCE" > "$CONFIG_OUTPUT"

echo "Validating config..."
circleci config validate "$CONFIG_OUTPUT"