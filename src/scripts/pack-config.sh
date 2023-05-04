#!/bin/bash

if  [ << parameters.branch >> != << pipeline.git.branch >> ]; then
    git checkout << parameters.branch >> << parameters.config-source >>
fi

echo "Packing config..."
circleci config pack << parameters.config-source >> > << parameters.config-output >>

echo "Validating config..."
circleci config validate << parameters.config-output >>