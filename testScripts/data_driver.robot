*** Settings ***
Documentation     Example test cases using a data-driver input file.

Test Template     Calculate
Library           CalculatorLibrary.py
Library           DataDriver  file=data_driver.csv  dialect=unix
Test Setup        Start Process
Test Teardown     Close Streams

*** Test Cases ***
Calculate ${expression} ${expected}



*** Keywords ***
Calculate
    [Arguments]    ${expression}    ${expected}
    Press Buttons    C${expression}=
    Result should be    ${expected}

Calculation should fail
    [Arguments]    ${expression}    ${expected}
    ${error} =    Should cause error    C${expression}=
    Should be equal    ${expected}    ${error}    # Using `BuiltIn` keyword
