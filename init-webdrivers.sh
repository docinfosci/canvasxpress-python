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
    CHROMIUM_BROWSER_INSTALL_EXIT=$?

    # If chromium-browser is not available try for older chromium
    if (("CHROMIUM_BROWSER_INSTALL_EXIT" != 0)); then
        echo "Cannot install chromium-browser, attempting to install chromium..."
        sudo apt-get -yq update; sudo apt-get -yq install --fix-missing chromium
        CHROMIUM_BROWSER_INSTALL_EXIT=$?

        # If chromium is also not available there's no point to continuing
        if (("CHROMIUM_BROWSER_INSTALL_EXIT" != 0)); then
            echo "Cannot install chromium, exiting build"
            exit 1
        
        # Otherwise verify the chromium installation
        else
            which chromium
            chromium --version

        fi

    # Otherwise verify the chromium-browser installation
    else
        which chromium-browser
        chromium-browser --version

    fi

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
