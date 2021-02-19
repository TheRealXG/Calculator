*** Settings ***
Documentation     Example test cases using the keyword-driven testing approach.
...
...               All tests contain a workflow constructed from keywords in
...               ``CalculatorLibrary.py``. Creating new tests or editing
...               existing is easy even for people without programming skills.
...
...               The _keyword-driven_ appoach works well for normal test
...               automation, but the _gherkin_ style might be even better
...               if also business people need to understand tests. If the
...               same workflow needs to repeated multiple times, it is best
...               to use to the _data-driven_ approach.
Library           CalculatorLibrary.py
Library           String
Test Setup        Start Process
Test Teardown     Close Streams

*** Test Cases ***


Add 2 Values
    Press Button    1
    Press Button    +
    Press Button    2
    Press Button    =
    Result should be    3

*** Comments ***
2 Digit Random Values
    ${val_1} =    Generate Random String    2    [NUMBERS]
    ${op} =    Generate Random String    1    +-*/
    ${val_2} =    Generate Random String    2    [NUMBERS]
    ${result} =    Calculate Expected Result    ${val_1}    ${op}    ${val_2}
    Log    ${val_1}${op}${val_2}=${result}'
    Press Buttons    ${val_1}${op}${val_2}=
    Result should be    ${result}

2 Digit Random Values Repeated, No /
    Repeat Keyword    5 times    Calculate with Random Values    2    2

Add Decimals
    Press Button    2
    Press Button    .
    Press Button    3
    Press Button    +
    Press Button    2
    Press Button    .
    Press Button    9
    Press Button    =
    Result should be    5.2

Subtract 2 Values
    Press Button    5
    Press Button    -
    Press Button    1
    Press Button    =
    Result should be    4

Multiply 2 Values
    Press Button    5
    Press Button    *
    Press Button    2
    Press Button    =
    Result should be    10

Divide 2 Values
    Press Button    6
    Press Button    /
    Press Button    2
    Press Button    =
    Result should be    3

Clear
    Press Button    1
    Press Button    C
    Result should be    0

Longer calculation
    Press Buttons    5 + 4 - 3 * 2 / 1 =
    Result should be    3

*** Keywords ***
Calculate with Random Values
    [Arguments]    ${num_digits_1}    ${num_digits_2}
    ${val_1} =    Generate Random String    2    [NUMBERS]
    ${op} =    Generate Random String    1    +-*
    ${val_2} =    Generate Random String    2    [NUMBERS]
    ${result} =    Calculate Expected Result    ${val_1}    ${op}    ${val_2}
    Log    ${val_1}${op}${val_2}=${result}'
    Press Buttons    ${val_1}${op}${val_2}=
    Result should be    ${result}
    [Return]    ${result}

Calculate Expected Result
    [Arguments]    ${value_1}    ${op}    ${value_2}
    ${value_1} =    Convert To Integer    ${value_1}
    ${value_2} =    Convert To Integer    ${value_2}
    ${expected} =    evaluate    (${value_1} ${op} ${value_2})
    [Return]    ${expected}
