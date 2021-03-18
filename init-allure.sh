#!/bin/bash

# Create directories and install services
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    ALLURE_VERSION="2.13.7"
    wget https://repo1.maven.org/maven2/io/qameta/allure/allure-commandline/${ALLURE_VERSION}/allure-commandline-${ALLURE_VERSION}.zip
    unzip allure-commandline-${ALLURE_VERSION}.zip
    mv allure-${ALLURE_VERSION} allure-commandline

elif [[ "$OSTYPE" == "darwin"* ]]; then
    mkdir -p ./allure-report

fi
