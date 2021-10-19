if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Install drivers for scipy installation
    sudo apt-get install gcc gfortran python3-dev libopenblas-dev liblapack-dev

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
