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

*** Test Cases ***
Add 2 Values
    Press Button    1
    Press button    +
    Press Button    2
    Press Button    =
    Result should be    3

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

