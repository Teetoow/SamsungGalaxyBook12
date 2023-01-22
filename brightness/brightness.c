/*
 *      brightness.c            (C) 2022-2023, Aurélien Croc (AP²C)
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
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "brightness.h"
#include "tables.h"


typedef struct {
    unsigned char               reg_26;
    unsigned char               reg_27;
    unsigned char               reg_28;
    unsigned char               reg_29;
    unsigned char               reg2_26;
} initData_t;



/* 
 * Communication with the display
 */
int _accessParaAuxRegs(aux_t aux)
{
    const char *cmd="PARAAUX-REG";

    for (int i=0; i < 5; i++) {
        char res;

        for (int i=0; cmd[i]; i++)
            dpAuxWrite(aux, 0x490, cmd[i]);
        res = dpAuxRead(aux, 0x490);
        printf("res=%i\n", (int)res);
        if (res > 0)
            return 0;
    }
    return 1;
}

dpWrite_t __getReg[] = {
    {0x491, 3, {2, 0x7F, 1}},
    {0x491, 3, {7, 0xFF, 4}},
    {0x492, 2, {3, 2, 0}},
    {0x492, 2, {6, 0, 0}},
    {0x492, 1, {0x0A, 0, 0}},
    {0, 0, {0, 0, 0}},
};

char __readDisplayRegister(aux_t aux, char reg, int type)
{
    char v;

    __getReg[2].val[1] = (type ? 4 : 2);
    __getReg[3].val[1] = reg;
    dpAuxWrites(aux, __getReg);
    return dpAuxRead(aux, 0x493);
}

dpWrite_t __getReg2[] = {
    {0x491, 3, {2, 0x7F, 1}},
    {0x491, 3, {7, 0xFF, 4}},
    {0x492, 2, {0, 0, 0}},
    {0x492, 2, {1, 0, 0}},
    {0x492, 2, {2, 0, 0}},
    {0x491, 2, {7, 0x0C, 0}},
    {0, 0, {0, 0, 0}},
};

char __readDisplayRegister2(aux_t aux, char val[3])
{
    char v;

    __getReg2[2].val[1] = val[0];
    __getReg2[3].val[1] = val[2];
    __getReg2[4].val[1] = val[1];
    dpAuxWrites(aux, __getReg2);
    return dpAuxRead(aux, 0x493);
}

void _readDisplayRegisters(aux_t aux, initData_t *data)
{
    data->reg_26 = __readDisplayRegister(aux, 0x26, 0);
    data->reg_27 = __readDisplayRegister(aux, 0x27, 0);
    data->reg_28 = __readDisplayRegister(aux, 0x28, 0);
    data->reg_29 = __readDisplayRegister(aux, 0x29, 0);
    data->reg2_26 = __readDisplayRegister(aux, 0x26, 1);
}



/*
 * Color profile management
 */
void _adjustColorProfile(initData_t *data)
{
    const char indexes[3] = {0x67, 0x69, 0x6B};
    int val[4], regsA, regsB, ptr;

    regsA = (data->reg_26 << 8) | data->reg_27;
    regsB = ((data->reg_28 << 8) | data->reg_29) << 10;

    val[0] = (regsB - (int)(44032 * regsA) / 40 + 46080) >> 10;
    val[1] = (regsB - (int)(317440 * regsA) / 297 - 3072) >> 10;
    val[2] = (regsB + (int)(375808 * regsA) / 84 - 16696320) >> 10;
    val[3] = (regsB + (int)(340992 * regsA) / 107 - 12693504) >> 10;

    // Compute the index
    if (val[0] <= 0) {
        if (val[1] >= 0)
            ptr = val[2] > 0 ? 6 : (val[3] >> 31) + 5;
        else
            ptr = val[2] > 0 ? 9 : (val[3] >> 31) + 8;
    } else
        ptr = val[2] > 0 ? 3 : (val[3] >> 31) + 2;
    if ((ptr - 1) > 8)
        ptr = 1;

    // Readjust color profiles
    for (int i=0; i < 3; i++) {
        char outA, outB, idx=indexes[i];

        outA = colorProfileAdjTableA[ptr*3 + i];
        outB = colorProfileAdjTableB[ptr*3 + i];
        colorProfile0[idx] = outB;
        colorProfile1[idx] = outA;
        colorProfile2[idx] = outB;
        colorProfile3[idx] = outA;
        colorProfile4[idx] = outA;
    }

}



/*
 * Brightness management
 */
char __brightnessRegisters[][3] = {
    {2, 0, 0},
    {2, 0, 0x80},
    {2, 1, 0},
    {2, 1, 0x80},
    {2, 2, 0},
    {2, 2, 0x80},
    {2, 3, 0},
    {2, 3, 0x80},
    {2, 4, 0},
    {2, 4, 0x80},
    {2, 5, 0},
    {4, 0, 0},
    {4, 0, 0x80},
    {4, 1, 0},
    {4, 1, 0x80},
    {4, 2, 0},
    {4, 2, 0x80},
    {4, 3, 0},
    {4, 3, 0x80},
    {4, 4, 0},
    {4, 4, 0x80},
    {4, 5, 0},
    {8, 0, 0},
    {8, 0, 0x80},
    {8, 1, 0},
    {8, 1, 0x80},
    {8, 2, 0},
    {8, 2, 0x80},
    {8, 3, 0},
    {8, 3, 0x80},
    {8, 4, 0},
    {8, 4, 0x80},
    {8, 5, 0},
};

void __readBrightnessRegisters(aux_t aux, int output[10][3])
{
    unsigned char val[33];

    // Read brightness registers
    for (int i=0; i < 33; i++)
        val[i] = __readDisplayRegister2(aux, __brightnessRegisters[i]);

    // Reorder by channel
    for (int i=0; i < 3; i++)
        output[0][i] = 0;
    output[1][0] = val[0x8];
    output[1][1] = val[0x13];
    output[1][2] = val[0x1E];
    for (int i=0; i < 8; i++) {
        output[i+2][0] = val[i];
        output[i+2][1] = val[i + 0xB];
        output[i+2][2] = val[i + 0x16];
    }
    if (val[9] >= 0x80)
        output[9][0] += 0x100;
    if (val[0x14] >= 0x80)
        output[9][1] += 0x100;
    if (val[0x1F] >= 0x80)
        output[9][2] += 0x100;
}

void __normalizeBrightnessRegisters(int valuesPerCh[10][3],double output[10][3])
{
	const int adj[3] = {0,0,0};

	// Fill the first row
	for (int i=0; i < 3; i++)
		output[0][i] = 7.2 - (valuesPerCh[0][i] + adj[i]) * 7.2 / 600.;

    // Normalize each channel for each element
	for (int i=9; i > 0; i--) {
        double maxValue;
        int shift;

        // Get adjustment factors
        shift = adjustmentFactor[i][0];
        maxValue = adjustmentFactor[i][1];

        for (int j=0; j < 3; j++) {
            int val = valuesPerCh[i][j] + shift;
            double highValue, maxRange;

            if (i < 9) {
                highValue = i == 1 ? 7.2 : output[0][j];
                maxRange = highValue - output[i+1][j];
            } else {
                highValue = 7.2;
                maxRange = highValue - 1.5;
            }
            output[i][j] = highValue - val * maxRange / maxValue;
        }
	}
}

void __computeThresholdValues(double normalizedRegisters[10][3], 
    double thresholdValues[0x100][3])
{
	double temp[2][3];

	// Parse each element
	for (int i=9; i > 0; i--) {
        int firstIdx, nItemsToFill;

        // Get the first index and the number of items to compute
        firstIdx = firstIdxPerGroup[i];
        nItemsToFill = firstIdx - firstIdxPerGroup[i-1];

        // Compute the delta for each channel
        for (int j=0; j < 3; j++) {
            double prevVal, val = normalizedRegisters[i][j];

            prevVal = i > 1 ? normalizedRegisters[i-1][j] : 7.2;
            temp[1][j] = val;
            temp[0][j] = (prevVal - val) / nItemsToFill;
        }

        // Fill the output table
        if (nItemsToFill)
            for (int j=0; j < nItemsToFill; j++)
                for (int k=0; k < 3; k++)
                    thresholdValues[firstIdx-j][k] = temp[1][k] + j * temp[0][k];
	}

    // Fill the first row
    for (int i=0; i < 3; i++)
        thresholdValues[0][i] = 7.2;
}


void __computeFractionPerBrightnessGroup(int slot, int highBrightnessMode, double output[10])
{
    double highestValue;
   
    // Set the extreme values
    output[0] = 0;
    if (highBrightnessMode)
        highestValue = highestValuePerBrightnessSlotHighMode[slot];
    else 
        highestValue = highestValuePerBrightnessSlotLowMode[slot];
    output[9] = highestValue;

    // Compute the intermediate values
    for (int i=1; i < 9; i++)
        output[i] = pow(firstIdxPerGroup[i] / 255., brightnessPowerTable[slot]) * highestValue;
}

void __getIndexOfFractionPerBrightnessGroup(int slot, 
    double fractionPerBrightnessGroup[10], int highBrightnessMode, 
    int output[10])
{
    output[0] = 0;

    for (int i=9; i > 0; i--) {
        double currentValue = fractionPerBrightnessGroup[i];
        int idx = 0;

        // Find the corresponding threshold
        while (idx < 0x100) {
            double threshold = brightnessThresholds[idx];

            // Does the threshold has been reached?
            if (threshold >= currentValue) {
                double delta;

                // Stop if it's the first element
                if (!idx)
                    break;

                // Otherwise compute the delta and check it
                delta = currentValue - brightnessThresholds[idx-1];
                if (delta < (threshold - currentValue))
                    idx--;
                break;
            }

            // Otherwise go to the next index
            idx++;
        }

        // Add the base index
        if (highBrightnessMode)
            idx += brightnessBaseIndexHighMode[slot*10 + i];
        else 
            idx += brightnessBaseIndexLowMode[slot*10 + i];
        output[i] = idx;
    }
}

void __getCorrespondingThresholds(int indexOfFractions[10],
    double thresholdValues[0x100][3], double output[10][3])
{
    for (int i=0; i < 10; i++) {
        int idx = indexOfFractions[i];

        for (int j=0; j < 3; j++)
            output[i][j] = thresholdValues[idx][j];
    }
}

void __thresholdsToRegisterValue(int slot, double thresholdValues[10][3], 
    int registerPerChannel[10][3], int highBrightnessMode, int output[10][3])
{
    for (int i=9; i > 0; i--) {
        double maxValue;
        int shift;

        // Get adjustment factors
        shift = adjustmentFactor[i][0];
        maxValue = adjustmentFactor[i][1];

        for (int j=0; j < 3; j++) {
            int val = thresholdValues[i][j];
            double highValue, maxRange;

            if (i < 9) {
                highValue = i == 1 ? 7.2 : thresholdValues[0][j];
                maxRange = highValue - thresholdValues[i+1][j];
            } else {
                highValue = 7.2;
                maxRange = highValue - 1.5;
            }

            val = ((int)(maxValue * (highValue - thresholdValues[i][j]) / 
                    maxRange)) - shift + 0.0005;

            if (highBrightnessMode)
                val += brightnessShiftFactorPerChannelHighMode[slot][i][j];
            else
                val += brightnessShiftFactorPerChannelLowMode[slot][i][j];

            if (val < 0)
                val = 0;
            if (val > 0xFF && i != 9)
                val = 0xFF;

            output[i][j] = val;
        }

    }
    // Init the first line of the table
    for (int i=0; i < 3; i++)
        output[0][i] = registerPerChannel[0][i];
}


void _prepareChannelAdjustmentTable(aux_t aux, displayBrightness_t* dp)
{
    double normalizedRegisters[10][3], thresholdValues[0x100][3];
    int registerPerChannel[10][3];
    int final[0x42][10][3];

	__readBrightnessRegisters(aux, registerPerChannel);
    __normalizeBrightnessRegisters(registerPerChannel, normalizedRegisters);
    __computeThresholdValues(normalizedRegisters, thresholdValues);
    for (int i=0; i < 0x42; i++) {
        double fractionPerBrightnessGroup[10], tempThresholdValues[10][3];
        int indexOfFractions[10];
        
        __computeFractionPerBrightnessGroup(i, dp->highBrightnessMode, 
            fractionPerBrightnessGroup);
        __getIndexOfFractionPerBrightnessGroup(i, fractionPerBrightnessGroup,
            dp->highBrightnessMode, indexOfFractions);
        __getCorrespondingThresholds(indexOfFractions, thresholdValues,
            tempThresholdValues);
        __thresholdsToRegisterValue(i, tempThresholdValues, registerPerChannel,
            dp->highBrightnessMode, final[i]);
    }

    // Reorder the result
    for (int i=0; i < 0x42; i++) {
		int ptr = 0;

		for (int j=0; j < 3; j++) {
			for (int k=0; k < 8; k++) {
                dp->channelAdjustment[i][ptr] = (char)final[i][k+2][j];
                ptr++;
			}
            dp->channelAdjustment[i][ptr] = (char)final[i][1][j];
            dp->channelAdjustment[i][ptr+1] = (char)((final[i][9][j] / 2)&0x80);
            dp->channelAdjustment[i][ptr+2] = (char)final[i][0][j];
            ptr += 3;
		}
	}

    /*for (int i=0; i < 0x42 * 11 * 3; i++)*/
            /*printf("%03u ", (unsigned int)(unsigned char)dp->channelAdjustment[i]);*/
}

displayBrightness_t* initBrightness(aux_t aux, int highBrightnessMode)
{
    displayBrightness_t* dp;
    initData_t data;

    if (_accessParaAuxRegs(aux))
        return NULL;

    // Create the structure which contains all the needed data
    dp = (displayBrightness_t *)malloc(sizeof(displayBrightness_t));
    memset(dp, 0, sizeof(displayBrightness_t));
    dp->highBrightnessMode = highBrightnessMode;

    _readDisplayRegisters(aux, &data);
    _adjustColorProfile(&data);
    _prepareChannelAdjustmentTable(aux, dp);

    dp->reg2_26 = data.reg2_26;

    return dp;
}

dpWrite_t __setBrightnessCmd[] = {{0x492, 2, {0x32, 1, 0}}};
void setBrightness(aux_t aux, displayBrightness_t *dp, char brightness)
{
    int ptr;

    if (brightness > 101)
        return;

    // Prepare new register values
    setBrightnessRegA[2].val[1] = valuesRegAPerBrightness[brightness];

    setBrightnessRegB[1].val[2] = valuesRegBPerBrightness[brightness][0];
    setBrightnessRegB[2].val[1] = valuesRegBPerBrightness[brightness][1];
    setBrightnessRegB[3].val[1] = valuesRegBPerBrightness[brightness][2];
    setBrightnessRegB[4].val[1] = valuesRegBPerBrightness[brightness][3];
    setBrightnessRegB[5].val[1] = valuesRegBPerBrightness[brightness][4];
    setBrightnessRegB[6].val[1] = valuesRegBPerBrightness[brightness][5];
    setBrightnessRegB[7].val[1] = valuesRegBPerBrightness[brightness][6];
    setBrightnessRegB[8].val[1] = valuesRegBPerBrightness[brightness][7];
    setBrightnessRegB[9].val[1] = valuesRegBPerBrightness[brightness][8];

    ptr = ptrIntoChannelAdjustmentTable[brightness];
    for (int i=0; i < 11*3; i++)
        setBrightnessRegD[i].val[1] = dp->channelAdjustment[ptr][i];

    // Set registers
    if (dp->highBrightnessMode) {
        setBrightnessRegC[1].val[1] = valuesRegCPerBrightness[brightness][0];
        setBrightnessRegC[2].val[1] = valuesRegCPerBrightness[brightness][1];
        setBrightnessRegC[4].val[1] = valuesRegC2PerBrightness[ptr];
        setBrightnessRegC[5].val[1] = dp->reg2_26;
        setBrightnessRegC[6].val[2] = brightness >= 0x64 ? 0x80 : 0x90;
        dpAuxWrites(aux, setBrightnessRegC);
    } else {
        if (!dp->lowBrightnessMode2) {
            setBrightnessRegE[2].val[1] = dp->reg2_26;
            dpAuxWrites(aux, setBrightnessRegE);
            usleep(1000);
            dpAuxWrites(aux, __setBrightnessCmd);
        }
        setBrightnessRegC_lowMode[1].val[1] = valuesRegCPerBrightness_lowMode
            [brightness][0];
        setBrightnessRegC_lowMode[2].val[1] = valuesRegCPerBrightness_lowMode
            [brightness][1];
        setBrightnessRegC_lowMode[3].val[2] = brightness >= 0x64 ? 0x80 : 0x90;
        dpAuxWrites(aux, setBrightnessRegC_lowMode);
    }

    dpAuxWrites(aux, setBrightnessRegD);
    usleep(1000);
    dpAuxWrites(aux, __setBrightnessCmd);
    dpAuxWrites(aux, setBrightnessRegA);
    dpAuxWrites(aux, setBrightnessRegB);
}

void setColorProfile(aux_t aux, displayBrightness_t *dp, char colorProfileNr)
{
    char *colorProfile;

    // Get the corresponding color profile values
    switch (colorProfileNr) {
        case 0: colorProfile = colorProfile0; break;
        case 1: colorProfile = colorProfile1; break;
        case 2: colorProfile = colorProfile2; break;
        case 3: colorProfile = colorProfile3; break;
        case 4: colorProfile = colorProfile4; break;
        case 5: colorProfile = colorProfile5; break;
        case 6: colorProfile = colorProfile6; break;
        default: colorProfile = colorProfile3; break;
    };

    // Recopy the register values and send it
    setColorProfileReg[0].val[2] = colorProfile[0];
    for (int i=1; i < 0x76; i++)
        setColorProfileReg[i].val[1] = colorProfile[i];
    dpAuxWrites(aux, setColorProfileReg);
}



/* vim: set expandtab tabstop=4 shiftwidth=4 smarttab tw=80 cin fenc=utf8 : */

