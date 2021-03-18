# Install the required Selenium drivers
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    export DEBIAN_FRONTEND=noninteractive
    export DEBIAN_PRIORITY=critical

    # Install the FireFox browser
    sudo apt-get -yq update; sudo apt-get -yq install --fix-missing xvfb
    sudo apt-get -yq update; sudo apt-get -yq install --fix-missing x11-utils
    sudo apt-get -yq update; sudo apt-get -yq install --fix-missing firefox
    which firefox
    firefox --version

    # Install the FireFox webdriver
    # https://github.com/mozilla/geckodriver/releases/
    wget https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-linux64.tar.gz
    tar xvfz geckodriver-v0.27.0-linux64.tar.gz
    sudo chmod +x geckodriver
    sudo mv geckodriver /usr/local/bin/
    which geckodriver
    geckodriver --version

    # Install the Chrome browser and webdriver
    sudo apt-get -yq update; sudo apt-get -yq install --fix-missing chromium-browser
    which chromium-browser
    chromium-browser --version

    sudo apt-get -yq update; sudo apt-get -yq install --fix-missing chromium-chromedriver
    which chromedriver
    chromedriver --version

elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Install tkinter
    brew reinstall tcl-tk

    # Install the FireFox webdriver
    brew reinstall geckodriver

    # Install the Chrome webdriver
    brew reinstall chromedriver
    sudo xattr -d com.apple.quarantine /usr/local/bin/chromedriver

else
    echo "Unkown OS -- manually install Selenium drivers such as for gecko"

fi
