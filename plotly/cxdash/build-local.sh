# This script builds the dash components.

#  Ensure the presence of a virtual environment
if ! [[ -d ./venv ]] ; then
    python3 -m venv ./venv
fi
source ./venv/bin/activate
python3 --version
sleep 2
python3 -m pip install -r ./requirements.txt

# Run the toolchain
export NODE_OPTIONS=--openssl-legacy-provider
npm run build
# npm run build:js
# dash-generate-components ./src/lib/components CXDash -p package-info.json

# Copy the Python package
cp -R ./cxdash ../../
