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
python setup.py bdist_wheel

# Only publish non-dev editions to PyPI
GIT_WORKING_BRANCH="$(git branch | grep \* | cut -d ' ' -f2)"
if [ $GIT_WORKING_BRANCH = "main" ]
then
  # Confirm the installation user account
  echo $TWINE_USERNAME

  # Acquire twine and push the package
  pip install twine
  twine upload --verbose -u $TWINE_USERNAME -p $TWINE_PASSWORD --repository-url https://tools-prd.aggregate-genius.com/python-packages/ ./dist/*
  TWINE_EXIT=$?

  # Fix for confirming status to the build server
  if (("$TWINE_EXIT" != 0))
  then
      exit 1
  fi

else
  # PyPI culture is that dev editions are not installed.
  echo "Edition is non-production so no installation performed"

fi

# We're finished with the virtual environment
deactivate
