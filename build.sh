#!/usr/bin/env bash

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

#  Ensure the presence of a virtual environment
if ! [[ -d ./venv ]] ; then
    python3 -m venv ./venv
fi
source ./venv/bin/activate

# Bootstrap Python
pip install -U -r ./requirements-project.txt
invoke init --dev --list

# Document the project
mkdocs build --clean --site-dir _build/html --config-file mkdocs.yml

# Test the project: goal is >= 90% coverage
invoke test
TEST_EXIT=$?

# Report results to SAAS platforms
invoke report

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

# If tests and static analysis pass then build and deploy
./distribute_package.sh
DISTRIBUTE_EXIT=$?
if (("$DISTRIBUTE_EXIT" != 0)); then
    echo "Deployment failed with code ${DISTRIBUTE_EXIT}"
    exit 1
fi

deactivate
