/* $******* SCADE Suite KCG 32-bit 6.6.1 beta (build i1) ********
** Command: kcg661.exe -config config.txt
** Generation date: 2020-11-18T09:40:16
*************************************************************$ */

#include "kcg_types.h"

#ifdef kcg_use_array_char_255
kcg_bool kcg_comp_array_char_255(array_char_255 *kcg_c1, array_char_255 *kcg_c2)
{
  kcg_bool kcg_equ;
  kcg_size kcg_ci;

  kcg_equ = kcg_true;
  for (kcg_ci = 0; kcg_ci < 255; kcg_ci++) {
    kcg_equ = kcg_equ & ((*kcg_c1)[kcg_ci] == (*kcg_c2)[kcg_ci]);
  }
  return kcg_equ;
}
#endif /* kcg_use_array_char_255 */

#ifdef kcg_use_array_char_254
kcg_bool kcg_comp_array_char_254(array_char_254 *kcg_c1, array_char_254 *kcg_c2)
{
  kcg_bool kcg_equ;
  kcg_size kcg_ci;

  kcg_equ = kcg_true;
  for (kcg_ci = 0; kcg_ci < 254; kcg_ci++) {
    kcg_equ = kcg_equ & ((*kcg_c1)[kcg_ci] == (*kcg_c2)[kcg_ci]);
  }
  return kcg_equ;
}
#endif /* kcg_use_array_char_254 */

/* $******* SCADE Suite KCG 32-bit 6.6.1 beta (build i1) ********
** kcg_types.c
** Generation date: 2020-11-18T09:40:16
*************************************************************$ */

