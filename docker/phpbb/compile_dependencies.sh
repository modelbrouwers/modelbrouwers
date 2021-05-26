#!/bin/bash

export CUSTOM_COMPILE_COMMAND="./compile_dependencies.sh"

pip-compile \
    --no-emit-index-url \
    "$@" \
    requirements.in
