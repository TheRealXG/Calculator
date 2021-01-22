#include "main.h"
#include "stdlib.h"
#include "stdio.h"

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

    int val_1, val_2;
    printf("Enter 1st Value, a whole number between 0 & 9:\n");
    scanf("%d", &val_1);
    
    switch(val_1) 
    {
        case 0:
            inC.keyEvent = KEY_00_Calc;
            break;
        case 1:
            inC.keyEvent = KEY_01_Calc;
            break;
        case 2:
            inC.keyEvent = KEY_02_Calc;
            break;
        case 3:
            inC.keyEvent = KEY_03_Calc;
            break;
        case 4:
            inC.keyEvent = KEY_04_Calc;
            break;
        case 5:
            inC.keyEvent = KEY_05_Calc;
            break;
        case 6:
            inC.keyEvent = KEY_06_Calc;
            break;
        case 7:
            inC.keyEvent = KEY_07_Calc;
            break;
        case 8:
            inC.keyEvent = KEY_08_Calc;
            break;
        case 9:
            inC.keyEvent = KEY_09_Calc;
            break;
        default:
            printf("Invalid Number\n");
            exit ( 0 );

    }
    root_Calc(&inC, &outC);
    printf("Display Output: %s\n", outC.outputDisplay);

    /* + */
    printf("Press +\n");
    inC.keyEvent = KEY_13_PLUS_Calc;
    root_Calc(&inC, &outC);
    printf("Display Output: %s\n", outC.outputDisplay);

    printf("Enter 2nd Value, a whole number between 0 & 9:\n");
    scanf("%d", &val_2);
    
    switch(val_2) 
    {
        case 0:
            inC.keyEvent = KEY_00_Calc;
            break;
        case 1:
            inC.keyEvent = KEY_01_Calc;
            break;
        case 2:
            inC.keyEvent = KEY_02_Calc;
            break;
        case 3:
            inC.keyEvent = KEY_03_Calc;
            break;
        case 4:
            inC.keyEvent = KEY_04_Calc;
            break;
        case 5:
            inC.keyEvent = KEY_05_Calc;
            break;
        case 6:
            inC.keyEvent = KEY_06_Calc;
            break;
        case 7:
            inC.keyEvent = KEY_07_Calc;
            break;
        case 8:
            inC.keyEvent = KEY_08_Calc;
            break;
        case 9:
            inC.keyEvent = KEY_09_Calc;
            break;
        default:
            printf("Invalid Number\n");
            exit ( 0 );

    }
    root_Calc(&inC, &outC);
    printf("Display Output: %s\n", outC.outputDisplay);

    /* = */
    printf("Press =\n");
    inC.keyEvent = KEY_12_EQUALS_Calc;
    root_Calc(&inC, &outC);
    printf("Final Output: %s.\n", outC.outputDisplay);

	exit( 0 );    
}

