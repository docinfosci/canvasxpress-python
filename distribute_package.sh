#!/usr/bin/env bash

# Ensure that we have a virtual environment
if ! [[ -d .venv ]] ; then
    python3 -m venv ./venv
fi
source ./venv/bin/activate

# Establish package components
rm -rf ./dist
python ./build_pkg_setup.py
python setup.py sdist

# Confirm the installation user account
echo $TWINE_USERNAME

# Acquire twine
pip install twine

# Only publish non-dev editions to PyPI
GIT_WORKING_BRANCH="$(git branch | grep \* | cut -d ' ' -f2)"
if [ $GIT_WORKING_BRANCH = "main" ]
then
  # Production deployment
  twine upload --verbose -u $TWINE_USERNAME -p $TWINE_PASSWORD --repository testpypi ./dist/*
  TWINE_EXIT=$?

else
  # Development deployment
  twine upload --verbose -u $TWINE_USERNAME -p $TWINE_PASSWORD --repository testpypi ./dist/*
  TWINE_EXIT=$?

fi

# We're finished with the virtual environment
deactivate

# Confirm status to the builder
if (("$TWINE_EXIT" != 0))
then
    exit 1
fi
