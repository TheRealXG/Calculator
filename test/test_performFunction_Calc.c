#ifdef TEST

#include "unity.h"

#include "performFunction_Calc.h"

#include "kcg_consts.h"


void setUp(void)
{
}

void tearDown(void)
{
}

void test_adding_function_adds(void)
{
    kcg_float32 val1 = 1;
    kcg_float32 val2 = 8;
    kcg_float32 expected = 6;
    kcg_int32 function = KEY_13_PLUS_Calc;
    kcg_float32 actual;
    
    actual = performFunction_Calc(val1,val2,function);
    
    TEST_ASSERT_EQUAL_FLOAT(expected, actual);
//    TEST_IGNORE_MESSAGE("Need to Implement performFunction_Calc");
}

#endif // TEST
