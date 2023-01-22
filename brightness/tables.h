/*
 *      tables.h                (C) 2022-2023, Aurélien Croc (AP²C)
 *
 *   This program is free software; you can redistribute it and/or modify it under
 *   the terms of the GNU General Public License as published by the Free Software
 *   Foundation; version 2 of the License.
 * 
 *   This program is distributed in the hope that it will be useful, but WITHOUT
 *   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 *   FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
 *   details.
 *   
 *   You should have received a copy of the GNU General Public License along with
 *   this program; If not, see <http://www.gnu.org/licenses/>.
 */
#ifndef TABLES_H
#define TABLES_H

#include "dpAux.h"



/*
 * Color profiles
 */
extern char colorProfile0[];
extern char colorProfile1[];
extern char colorProfile2[];
extern char colorProfile3[];
extern char colorProfile4[];
extern char colorProfile5[];
extern char colorProfile6[];

extern char colorProfileAdjTableA[];
extern char colorProfileAdjTableB[];



/*
 * Brightness management
 */
extern int adjustmentFactor[10][2];
extern int firstIdxPerGroup[10];
extern int highestValuePerBrightnessSlotHighMode[];
extern int highestValuePerBrightnessSlotLowMode[];
extern double brightnessPowerTable[];
extern double brightnessThresholds[];
extern int brightnessBaseIndexHighMode[];
extern int brightnessBaseIndexLowMode[];
extern int brightnessShiftFactorPerChannelHighMode[0x42][10][3];
extern int brightnessShiftFactorPerChannelLowMode[0x42][10][3];



/*
 * Brightness and color profile registers settings
 */
extern dpWrite_t setBrightnessRegA[];
extern dpWrite_t setBrightnessRegB[];
extern dpWrite_t setBrightnessRegC[];
extern dpWrite_t setBrightnessRegC_lowMode[];
extern dpWrite_t setBrightnessRegD[];
extern dpWrite_t setBrightnessRegE[];
extern dpWrite_t setColorProfileReg[];

extern int ptrIntoChannelAdjustmentTable[];
extern char valuesRegAPerBrightness[];
extern char valuesRegBPerBrightness[][9];
extern char valuesRegCPerBrightness[][2];
extern char valuesRegCPerBrightness_lowMode[][2];
extern char valuesRegC2PerBrightness[];


#endif /* TABLES_H */

/* vim: set expandtab tabstop=4 shiftwidth=4 smarttab tw=80 cin fenc=utf8 : */

