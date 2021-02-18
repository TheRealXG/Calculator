#include "main.h"
#include "stdlib.h"
#include "stdio.h"
#include "string.h"
#include "stdbool.h"

/*Allocate the controller memory*/
inC_root_Calc inC;
outC_root_Calc outC;
bool flag; // Flag for GDB to pass input to the Calculator. Requires calc.exe to be compiled without -02 optimization for GDB to use this.
char input;

rtems_task Init(
  rtems_task_argument ignored
)
{
    /*Initialize the memory*/
    root_init_Calc(&outC);
    flag = true; // Wait for input

    
    /*Executive Loop: 
      for this demo we hardcode a finite sequence of key presses*/
    inC.keyEvent = KEY_19_NONE_Calc;
    root_Calc(&inC, &outC);
    printf("Display Output: %s\n", outC.outputDisplay);
    
    printf("Press Button (No negatives; C to clear, q to Quit):\n");
    while(true)
    {
        if(!flag)
        {
            printf("Input value: %c\n", input);

            if(input == '0')
            {
                inC.keyEvent = KEY_00_Calc;
            }else if(input == '1')
            {
                inC.keyEvent = KEY_01_Calc;
            }else if(input == '2')
            {
                inC.keyEvent = KEY_02_Calc;
            }else if(input == '3')
            {
                inC.keyEvent = KEY_03_Calc;
            }else if(input == '4')
            {
                inC.keyEvent = KEY_04_Calc;
            }else if(input == '5')
            {
                inC.keyEvent = KEY_05_Calc;
            }else if(input == '6')
            {
                inC.keyEvent = KEY_06_Calc;
            }else if(input == '7')
            {
                inC.keyEvent = KEY_07_Calc;
            }else if(input == '8')
            {
                inC.keyEvent = KEY_08_Calc;
            }else if(input == '9')
            {
                inC.keyEvent = KEY_09_Calc;
            }else if(input == '+')
            {
                inC.keyEvent = KEY_13_PLUS_Calc;
            }else if(input == '-')
            {
                inC.keyEvent = KEY_14_MINUS_Calc;
            }else if(input == '*')
            {
                inC.keyEvent = KEY_15_TIMES_Calc;
            }else if(input == '/')
            {
                inC.keyEvent = KEY_16_DIVIDE_Calc;
            }else if(input == 'C')
            {
                inC.keyEvent = KEY_18_CLEAR_ALL_Calc;
            }else if(input == '.')
            {
                inC.keyEvent = KEY_10_DECIMAL_Calc;
            }else if(input == '=')
            {
                inC.keyEvent = KEY_12_EQUALS_Calc;
            }else
            {
                printf("Invalid Input\n");
                exit ( 0 );
            }
            
            root_Calc(&inC, &outC);
            printf("Display Output: %s\n", outC.outputDisplay);
            flag = true; //Rest flag to 1 so doesn't enter If statement
        } else if (flag)
        {
            //printf("Flag == true\n");
        } else
        {
            //printf("Flag is default. %d\n", flag);
        }

        
    }

	exit( 0 );    
}

