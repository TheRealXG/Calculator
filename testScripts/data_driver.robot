*** Settings ***
Documentation     Example test cases using a data-driver input file.
...               This reads in a CSV file and uses the columns as
...               arguments for the Test Case, as in the Data Driven tests.
Test Template     Calculate
Library           CalculatorLibrary.py  "build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe"
Library           DataDriver    file=data_driver.csv    dialect=unix
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
