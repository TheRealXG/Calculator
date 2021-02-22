*** Settings ***
Documentation     Example test cases using the data-driven testing approach.
...
...               The _data-driven_ style works well when you need to repeat
...               the same workflow multiple times.
...               Note: Setup and Teardown are performed for each Test Case,
...               e.g. Addition, not for each expression within the Test Case.
...
...               Tests use ``Calculate`` keyword created in this file, that in
...               turn uses keywords in ``CalculatorLibrary.py``. An exception
...               is the last test that has a custom _template keyword_.
Test Template     Calculate
Library           CalculatorLibrary.py  "build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe"
Test Setup        Start Process
Test Teardown     Close Streams

*** Test Cases ***    Expression    Expected
Addition              12 + 2        14
                      2 + 3         5

Subtraction           12 - 2        10
                      2 - 3         -1

Multiplication        12 * 2        24
                      2 * .5        1

Division              12 / 2        6
                      2 / 4         0.5

Failing               1 + 1         3

Calculation error     [Template]    Calculation should fail
                      w             Invalid Input
                      p             Invalid Input

*** Keywords ***
Calculate
    [Arguments]    ${expression}    ${expected}
    Press Buttons    C${expression}=
    Result should be    ${expected}

Calculation should fail
    [Arguments]    ${expression}    ${expected}
    ${error} =    Should cause error    C${expression}=
    Should be equal    ${expected}    ${error}    # Using `BuiltIn` keyword
