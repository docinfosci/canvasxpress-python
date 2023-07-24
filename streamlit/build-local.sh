# This script builds the streamlit components.

#  Ensure the presence of a virtual environment
if ! [[ -d ./venv ]] ; then
    python3 -m venv ./venv
fi
source ./venv/bin/activate
pip install -r ./requirements.txt

# Build the React component
# shellcheck disable=SC2164
cd ./cxstreamlit/frontend/
npm install
npm run build
cd ../../../

# Copy the Python package
mkdir -p cxstreamlit/frontend/
cp -R streamlit/cxstreamlit/frontend/build cxstreamlit/frontend/
cp -R streamlit/cxstreamlit/frontend/*.json cxstreamlit/frontend/
cp -R streamlit/cxstreamlit/frontend/*.js cxstreamlit/frontend/
cp -R streamlit/cxstreamlit/*.py cxstreamlit/

ls -lah cxstreamlit
ls -lah cxstreamlit/frontend/
ls -lah cxstreamlit/frontend/build/