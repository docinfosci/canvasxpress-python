# CircleCI is used for official testing and handles  Linux installations.

# Install the required Selenium drivers
if [[ "$OSTYPE" == "darwin"* ]]; then
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
