/* $******* SCADE Suite KCG 32-bit 6.6.1 beta (build i1) ********
** Command: kcg661.exe -config config.txt
** Generation date: 2020-11-18T09:40:16
*************************************************************$ */
#ifndef _root_Calc_H_
#define _root_Calc_H_

#include "kcg_types.h"
#include "kcg_imported_functions.h"
#include "performFunction_Calc.h"
#include "valueEntry_Calc.h"

/* ========================  input structure  ====================== */
typedef struct { kcg_int32 /* keyEvent/ */ keyEvent; } inC_root_Calc;

/* =====================  no output structure  ====================== */

/* ========================  context type  ========================= */
typedef struct {
  /* ---------------------------  outputs  --------------------------- */
  array_char_255 /* outputDisplay/ */ outputDisplay;
  /* -----------------------  no local probes  ----------------------- */
  /* ----------------------- local memories  ------------------------- */
  SSM_ST_SM1 /* SM1: */ SM1_state_nxt;
  kcg_float32 /* entryValue/ */ entryValue;
  kcg_int32 /* storedFunction/ */ storedFunction;
  kcg_float32 /* storedValue/ */ storedValue;
  /* ---------------------  sub nodes' contexts  --------------------- */
  outC_valueEntry_Calc /* SM1:EnterValue1:_L1=(Calc::valueEntry#1)/ */ Context_valueEntry_1;
  outC_valueEntry_Calc /* SM1:EnterValue2:_L1=(Calc::valueEntry#2)/ */ Context_valueEntry_2;
  /* ----------------- no clocks of observable data ------------------ */
} outC_root_Calc;

/* ===========  node initialization and cycle functions  =========== */
/* Calc::root/ */
extern void root_Calc(inC_root_Calc *inC, outC_root_Calc *outC);

#ifndef KCG_NO_EXTERN_CALL_TO_RESET
extern void root_reset_Calc(outC_root_Calc *outC);
#endif /* KCG_NO_EXTERN_CALL_TO_RESET */

#ifndef KCG_USER_DEFINED_INIT
extern void root_init_Calc(outC_root_Calc *outC);
#endif /* KCG_USER_DEFINED_INIT */



#endif /* _root_Calc_H_ */
/* $******* SCADE Suite KCG 32-bit 6.6.1 beta (build i1) ********
** root_Calc.h
** Generation date: 2020-11-18T09:40:16
*************************************************************$ */

