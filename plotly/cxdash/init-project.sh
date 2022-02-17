# This script initializes the work environment for the Plotly Dash CanvasXpress components.

#  Ensure the presence of a virtual environment
if ! [[ -d ./venv ]] ; then
    python3 -m venv ./venv
fi
source ./venv/bin/activate

# Ensure that node.js is available.
if [[ "$OSTYPE" == "linux-gnu"* ]]
then
    export DEBIAN_FRONTEND=noninteractive
    export DEBIAN_PRIORITY=critical

    sudo apt update
    sudo apt install --fix-missing -yq nodejs npm
    node -v

elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install nodejs
    node -v

else
    echo "Unkown OS -- manually install Selenium drivers such as for gecko"

fi

# Ensure that essential project utilities are available
pip install -U pip setuptools wheel
pip install -U -r requirements.txt

npm install canvasxpress
npm install canvasxpress-react
