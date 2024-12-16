#!/usr/bin/env bash

#  Ensure the presence of a virtual environment
if ! [[ -d ./venv ]] ; then
    python3 -m venv ./venv
fi
source ./venv/bin/activate

# Track which profile should be used for work
GIT_WORKING_BRANCH="$(git branch | grep \* | cut -d ' ' -f2)"
if [ $GIT_WORKING_BRANCH = "main" ]
then
    BRANCH_STAGE=${BRANCH_STAGE:="master"}
else
    BRANCH_STAGE=${BRANCH_STAGE:="develop"}
fi
echo "Source edition matches '${BRANCH_STAGE}' (branch '${GIT_WORKING_BRANCH}')"

# Install essential packages
chmod +x ./*.sh
./init-drivers.sh

# Bootstrap Python
python3 ./build_pkg_setup.py
pip install --no-cache-dir -U -r ./requirements-project.txt
invoke init --dev --list

# Build Dash components
cd plotly/cxdash/
./init-project.sh
./build-local.sh
cd ../../

# Force conformance to project styles (see pyproject,toml)
# We will manually perform formatting here and there, as the latest black breaks the doc generation.
# black --safe canvasxpress cxdash tests

# Test the project: goal is >= 90% coverage
invoke test
TEST_EXIT=$?

# Static analysis: goal is PEP compliance
prospector \
    --zero-exit \
    --show-profile \
    --no-autodetect \
    --strictness low \
    -o text \
    ./canvasxpress
PROSPECTOR_EXIT=$?

# Alert user at end of build as to failures preventing distribution
if (("$TEST_EXIT" != 0)); then
    echo "Tests failed with code ${TEST_EXIT}"
    exit 1
fi
if (("PROSPECTOR_EXIT" != 0)); then
  echo "Static analysis failed with code ${PROSPECTOR_EXIT}"
  exit 1
fi

# Generate documentation - deprecated, switching to alternate format.
# ./build_docs.sh

deactivate
