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
cd ./../../

# Copy the Python package
rm -rf ./../cxstreamlit
cp -R ./cxstreamlit ./../cxstreamlit
rm -rf \
  ./../cxstreamlit/frontend/public \
  ./../cxstreamlit/frontend/src \
  ./../cxstreamlit/frontend/node_modules \
  ./../cxstreamlit/frontend/.* \
  ./../cxstreamlit/frontend/tsconfig.json
