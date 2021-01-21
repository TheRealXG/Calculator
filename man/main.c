#include "main.h"

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
    printf("output: %s\n", outC.outputDisplay);

    /* 1 */
    inC.keyEvent = KEY_01_Calc;
    root_Calc(&inC, &outC);
    printf("output: %s\n", outC.outputDisplay);

    /* + */
    inC.keyEvent = KEY_13_PLUS_Calc;
    root_Calc(&inC, &outC);
    printf("output: %s\n", outC.outputDisplay);

    /* 2 */
    inC.keyEvent = KEY_02_Calc;
    root_Calc(&inC, &outC);
    printf("output: %s\n", outC.outputDisplay);

    /* = */
    inC.keyEvent = KEY_12_EQUALS_Calc;
    root_Calc(&inC, &outC);
    printf("output: %s\n", outC.outputDisplay);

	exit( 0 );    
}

