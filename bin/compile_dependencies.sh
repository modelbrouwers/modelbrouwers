#!/bin/bash

set -ex

toplevel=$(git rev-parse --show-toplevel)

cd $toplevel

# Base deps
pip-compile \
    --no-index \
    requirements/base.in

# Travis/tests deps
pip-compile \
    --no-index \
    --output-file requirements/test.txt \
    requirements/base.txt \
    requirements/test.in
