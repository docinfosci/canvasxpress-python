#!/usr/bin/env bash

# Ensure that we have a virtual environment
if ! [[ -d .venv ]] ; then
    python3 -m venv ./venv
fi
source ./venv/bin/activate

# Establish package components
rm -rf ./dist
python ./generate_setup_instructions.py
python setup.py sdist
python setup.py bdist

# Confirm the installation user account
echo $TWINE_USERNAME

# Acquire twine and push the package
pip install twine
twine upload --verbose -u $TWINE_USERNAME -p $TWINE_PASSWORD --repository-url https://tools-prd.aggregate-genius.com/python-packages/ ./dist/*
TWINE_EXIT=$?

# We're finished with the virtual environment
deactivate

# Fix for confirming status to the build server
if (("$TWINE_EXIT" != 0)); then
    exit 1
fi
