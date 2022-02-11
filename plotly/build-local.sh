# This script builds the dash components.

#  Ensure the presence of a virtual environment
if ! [[ -d ./venv ]] ; then
    python3 -m venv ./venv
fi
source ./venv/bin/activate

# Run the toolchain
npm run build
# npm run build:js
# dash-generate-components ./src/lib/components CXDash -p package-info.json
