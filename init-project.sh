#!/bin/bash

chmod +x ./init-webdrivers.sh
./init-webdrivers.sh

# Install the essential Python packages
if ! [[ -d ./venv ]] ; then
    python3 -m venv ./venv
fi
source ./venv/bin/activate

pip install --no-cache-dir  -U -r ./requirements-project.txt
invoke init --dev --list

deactivate
