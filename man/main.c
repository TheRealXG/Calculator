#include "main.h"
#include "stdlib.h"
#include "stdio.h"
#include "string.h"
#include "stdbool.h"

/*Allocate the controller memory*/
inC_root_Calc inC;
outC_root_Calc outC;

rtems_task Init(
  rtems_task_argument ignored
)
{
    /*Initialize the memory*/
    root_init_Calc(&outC);

    
    /*Executive Loop: 
      for this demo we hardcode a finite sequence of key presses*/
    inC.keyEvent = KEY_19_NONE_Calc;
    root_Calc(&inC, &outC);
    printf("Display Output: %s\n", outC.outputDisplay);

    char input;
    while(true)
    {
        printf("Press Button (No negatives; C to clear, q to Quit):\n");
        scanf("%s", &input);
        
        if(strcmp(&input,"0") == 0)
        {
            inC.keyEvent = KEY_00_Calc;
             
        }else if(strcmp(&input,"1") == 0)
        {
            inC.keyEvent = KEY_01_Calc;
        }else if(strcmp(&input,"2") == 0)
        {
            inC.keyEvent = KEY_02_Calc;
        }else if(strcmp(&input,"3") == 0)
        {
            inC.keyEvent = KEY_03_Calc;
        }else if(strcmp(&input,"4") == 0)
        {
            inC.keyEvent = KEY_04_Calc;
        }else if(strcmp(&input,"5") == 0)
        {
            inC.keyEvent = KEY_05_Calc;
        }else if(strcmp(&input,"6") == 0)
        {
            inC.keyEvent = KEY_06_Calc;
        }else if(strcmp(&input,"7") == 0)
        {
            inC.keyEvent = KEY_07_Calc;
        }else if(strcmp(&input,"8") == 0)
        {
            inC.keyEvent = KEY_08_Calc;
        }else if(strcmp(&input,"9") == 0)
        {
            inC.keyEvent = KEY_09_Calc;
        }else if(strcmp(&input,"+") == 0)
        {
            inC.keyEvent = KEY_13_PLUS_Calc;
        }else if(strcmp(&input,"-") == 0)
        {
            inC.keyEvent = KEY_14_MINUS_Calc;
        }else if(strcmp(&input,"*") == 0)
        {
            inC.keyEvent = KEY_15_TIMES_Calc;
        }else if(strcmp(&input,"/") == 0)
        {
            inC.keyEvent = KEY_16_DIVIDE_Calc;
        }else if(strcmp(&input,"C") == 0)
        {
            inC.keyEvent = KEY_18_CLEAR_ALL_Calc;
        }else if(strcmp(&input,".") == 0)
        {
            inC.keyEvent = KEY_10_DECIMAL_Calc;
        }else if(strcmp(&input,"=") == 0)
        {
            inC.keyEvent = KEY_12_EQUALS_Calc;
        }else
        {
            printf("Invalid Input\n");
            exit ( 0 );
        }
        
        root_Calc(&inC, &outC);
        printf("Display Output: %s\n", outC.outputDisplay);
    }

	exit( 0 );    
}

