#!/usr/bin/python3
#
#    brightness.py             (C) 2022-2023, Aurélien Croc (AP²C)
#
#  This program is free software; you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free Software
#  Foundation; version 2 of the License.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#  
#  You should have received a copy of the GNU General Public License along with
#  this program; If not, see <http://www.gnu.org/licenses/>.
from dpAux import DPAux
from tables import *
from time import sleep, time
import threading
import fcntl
import signal
import sys
import os

displayInfo = {}
BACKLIGHT_PATH = '/sys/class/backlight/intel_backlight'
BRIGHTNESS_PATH = os.path.join(BACKLIGHT_PATH, 'brightness')
MAX_BRIGHTNESS_PATH = os.path.join(BACKLIGHT_PATH, 'max_brightness')

def sendParaAux(aux) :
    for i in range(0, 5) :
        for c in 'PARAAUX-REG' :
            aux.write(0x490, ord(c))
        val = aux.read(0x490)
        if val > 0 :
            return True
    return False

def endParaAux(aux) :
    for c in '0000' :
        aux.write(0x490, ord(c))

def readDisplayRegister(aux, reg) :
    aux.writeArray(( \
        (0x491, 2), \
        (0x492, 0x7F), \
        (0x493, 1), \
        (0x491, 7), \
        (0x492, 0xFF), \
        (0x493, 4), \
        (0x492, 3), \
        (0x493, 2), \
        (0x492, 6), \
        (0x493, reg), \
        (0x492, 0x0A), \
    ))
    return aux.read( 0x493)

def readDisplayRegister3(aux, reg) :
    aux.writeArray(( \
        (0x491, 2), \
        (0x492, 0x7F), \
        (0x493, 1), \
        (0x491, 7), \
        (0x492, 0xFF), \
        (0x493, 4), \
        (0x492, 3), \
        (0x493, 4), \
        (0x492, 6), \
        (0x493, reg), \
        (0x492, 0x0A), \
    ))
    return aux.read( 0x493)

def readDisplayRegister2(aux, valA, valB, valC) :
    aux.writeArray(( \
        (0x491, 2), \
        (0x492, 0x7F), \
        (0x493, 1), \
        (0x491, 7), \
        (0x492, 0xFF), \
        (0x493, 4), \
        (0x492, 0), \
        (0x493, valA), \
        (0x492, 1), \
        (0x493, valC), \
        (0x492, 2), \
        (0x493, valB), \
        (0x491, 7), \
        (0x492, 0x0C), \
    ))
    return aux.read( 0x493)

def getDisplayRegisters(aux, displayInfo) :
    displayInfo['reg_23'] = readDisplayRegister(aux, 0x23)
    displayInfo['reg_24'] = readDisplayRegister(aux, 0x24)
    displayInfo['reg_25'] = readDisplayRegister(aux, 0x25)

def getDisplayRegisters2(aux, displayInfo) :
    displayInfo['reg_26'] = readDisplayRegister(aux, 0x26)
    displayInfo['reg_27'] = readDisplayRegister(aux, 0x27)
    displayInfo['reg_28'] = readDisplayRegister(aux, 0x28)
    displayInfo['reg_29'] = readDisplayRegister(aux, 0x29)

    displayInfo['reg_2A'] = readDisplayRegister(aux, 0x2a)
    displayInfo['reg_2B'] = readDisplayRegister(aux, 0x2b)

    displayInfo['reg2_21'] = readDisplayRegister3(aux, 0x21)
    displayInfo['reg2_22'] = readDisplayRegister3(aux, 0x22)
    displayInfo['reg2_23'] = readDisplayRegister3(aux, 0x23)
    displayInfo['reg2_24'] = readDisplayRegister3(aux, 0x24)
    displayInfo['reg2_25'] = readDisplayRegister3(aux, 0x25)
    displayInfo['reg2_26'] = readDisplayRegister3(aux, 0x26)
    displayInfo['reg2_27'] = readDisplayRegister3(aux, 0x27)


def initBrightnessTable340(aux, displayInfo) :
    result = []
    for (valA, valB, valC) in registerValuesA :
        result.append(readDisplayRegister2(aux, valA, valB, valC))
    displayInfo['table340'] = result

def __reorderTable340(inputTable) :
    # Create a 0 filled table
    output = [0] * 30

    # Fill the first row
    output[3] = inputTable[0x8]
    output[4] = inputTable[0x13]
    output[5] = inputTable[0x1E]

    # Fill the other rows
    counter = 6
    j = 0
    while counter <= 0x1B :
        output[counter] = inputTable[j]
        output[counter+1] = inputTable[j + 0xB]
        output[counter+2] = inputTable[j + 0x16]
        counter += 3
        j += 1
        if j > 7 :
            break

    # Readapt the last row
    if inputTable[0x9] >= 0x80 :
        output[0x1b] += 0x100
    if inputTable[0x14] >= 0x80 :
        output[0x1c] += 0x100
    if inputTable[0x1F] >= 0x80 :
        output[0x1d] += 0x100

    return output


def __computeScaleFactorFromVectorized340(reordered340) :
    # Create a 0 filled table
    output = [0] * 30

    # Fill the first row
    for i in range(3) :
        tmp = scalarVectorA[reordered340[i] + adjustmentFactorA[i]]
        output[i] = 7.2 - tmp * 7.2 / 600.; 

    # Fill the other rows
    counter = 9 # == r8
    while counter > 0 :
        ebp = adjustmentFactorB[(counter-1)*2]
        xmm4 = adjustmentFactorB[counter*2 - 1]

        for i in range(3) :
            xmm1 = adjustmentFactorA[counter*3 + i] + reordered340[counter*3 + i] + ebp
            if counter != 1 and counter != 9 :
                xmm2 = output[i]
                xmm1 = xmm1 * (xmm2 - output[(counter+1)*3 + i]) / xmm4
                output[counter*3 + i] = xmm2 - xmm1
            else :
                if counter == 1 :
                    xmm0 = 7.2 - output[(counter+1) * 3 + i]
                    ptr = 3 + i
                else :
                    xmm0 = 7.2 - 1.5
                    ptr = 27 + i
                output[counter*3 + i] = 7.2 - xmm1 * xmm0 / xmm4
        counter -= 1

    return output

scaleFactor2 = (0, 3, 0xB, 0x17, 0x23, 0x33, 0x57, 0x97, 0xCB, 0xFF)
    

def __computeFractionalValueTable(scaleFactor) :
    # Create a 0 filled table and a temp table
    output = [0] * (0x100*3)
    temp = [0] * 33

    # Parse each row
    counter = 9
    temp[0] = 7.2
    while counter > 0:
        nElements = scaleFactor2[counter]
        nItemsToFill = nElements - scaleFactor2[counter-1]

        # Compute the delta for each column
        ptr = (counter - 1) * 3
        for i in range(3) :
            val1 = scaleFactor[ptr + i + 3]
            #temp[(9-counter)*3 + i + 3  +1] = val1
            temp[i + 3  +1] = val1
            delta = scaleFactor[ptr + i] - val1
            #temp[(9-counter)*3 + i +1] = delta
            temp[i +1] = delta

        
        # Special case for the last row
        if counter == 1 :
            for i in range(3) :
                temp[i+1] = 7.2 - scaleFactor[ptr + i + 3]

        # Fill the output table
        if nItemsToFill :
            for i in range(nItemsToFill) :
                for j in range(3) :
                    output[(nElements-i)*3 + j] = i * temp[j+1] / nItemsToFill + temp[j+1 + 3]
        counter -= 1

    # Fill the last row
    output[0] = temp[0]
    output[1] = temp[0]
    output[2] = temp[0]

    return output


brightLastValueCC5True = (0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73,
    0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 
    0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 
    0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x73, 0x7A, 0x83, 0x8A, 0x94,
    0x9C, 0xA4, 0xAF, 0xBA, 0xC6, 0xD1, 0xDC, 0xEC, 0xFA, 0xFA, 0xFA, 0xFA, 
    0xFA, 0xFA, 0xFA, 0x109, 0x11B, 0x12C, 0x13E, 0x150, 0x168, 0x168)

brightLastValueCC5False = (0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D,
    0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 
    0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x6D,
    0x6D, 0x6D, 0x6D, 0x6D, 0x6D, 0x72, 0x7A, 0x81, 0x8C, 0x94, 0x9C, 0xA7,
    0xB0, 0xBB, 0xC5, 0xD1, 0xDD, 0xE8, 0xF6, 0x104, 0x104, 0x104, 0x104, 
    0x104, 0x104, 0x104, 0x113, 0x123, 0x130, 0x141, 0x150, 0x168, 0x168)

brightPowerTable = (2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15,
    2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15,
    2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15,
    2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15,
    2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15,
    2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15,
    2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15,
    2.15, 2.2, 2.2)


def __computeTemp10DoubleTable(counterNr, isCC5True) :
    # Create a 0 filled table
    output = [0] * (10)

    # Set the last value
    if isCC5True :
        output[9] = brightLastValueCC5True[counterNr]
    else :
        output[9] = brightLastValueCC5False[counterNr]

    # Compute the others
    i = 8
    while i > 0 :
        output[i] = pow(scaleFactor2[i] / 255., brightPowerTable[counterNr]) * output[9]
        i -= 1

    return output


brightComparisonValues = (0.0, 0.0018277, 0.0083981, 0.0204918, 0.0385875,
    0.06304460000000001, 0.0941558, 0.1321691, 0.1773014, 0.2297458, 0.2896771,
    0.3572547, 0.4326262, 0.5159285, 0.6072895, 0.7068298, 0.8146631, 0.9308972,
    1.0556346, 1.1889731, 1.3310062, 1.4818238, 1.6415118, 1.8101532, 1.9878281,
    2.1746137, 2.3705847, 2.5758133, 2.7903699, 3.0143224, 3.2477371, 3.4906783,
    3.7432088, 4.0053897, 4.2772804, 4.5589392, 4.8504229, 5.151787, 5.4630857,
    5.7843723, 6.1156988, 6.457116, 6.808674, 7.1704218, 7.5424075, 7.9246782,
    8.317280200000001, 8.7202591, 9.133659700000001, 9.557525800000001, 9.9919008,
    10.4368272, 10.8923468, 11.3585009, 11.8353301, 12.3228744, 12.8211731,
    13.3302651, 13.8501887, 14.3809816, 14.922681, 15.4753237, 16.0389458,
    16.6135833, 17.1992713, 17.7960447, 18.403938, 19.0229852, 19.6532198,
    20.2946751, 20.9473839, 21.6113786, 22.2866912, 22.9733535, 23.6713969,
    24.3808523, 25.1017504, 25.8341216, 26.5779959, 27.333403, 28.1003724,
    28.8789331, 29.6691141, 30.4709439, 31.2844506, 32.1096625, 32.9466071,
    33.7953119, 34.6558043, 35.5281111, 36.4122591, 37.3082748, 38.2161844,
    39.136014, 40.0677893, 41.011536, 41.9672794, 42.9350447, 43.9148567,
    44.9067403, 45.91072, 46.9268201, 47.9550647, 48.9954779, 50.0480833,
    51.1129046, 52.1899652, 53.2792883, 54.3808969, 55.4948139, 56.621062,
    57.7596639, 58.9106417, 60.0740179, 61.2498144, 62.4380531, 63.6387558,
    64.8519441, 66.0776394, 67.3158632, 68.56663639999999, 69.8299801,
    71.10591530000001, 72.39446270000001, 73.6956428, 75.0094761, 76.33598310000001,
    77.67518389999999, 79.02709849999999, 80.391747, 81.7691492, 83.15932479999999,
    84.56229329999999, 85.9780743, 87.40668719999999, 88.8481511, 90.3024851,
    91.7697084, 93.2498397, 94.7428979, 96.2489017, 97.7678696, 99.29982,
    100.8447715, 102.4027422, 103.9737502, 105.5578137, 107.1549506, 108.7651787,
    110.3885158, 112.0249797, 113.6745877, 115.3373576, 117.0133065, 118.7024519,
    120.4048109, 122.1204006, 123.8492381, 125.5913403, 127.346724, 129.1154061,
    130.8974033, 132.692732, 134.5014089, 136.3234503, 138.1588727, 140.0076924,
    141.8699254, 143.745588, 145.6346961, 147.5372658, 149.453313, 151.3828534,
    153.3259029, 155.282477, 157.2525914, 159.2362616, 161.233503, 163.2443312,
    165.2687613, 167.3068086, 169.3584883, 171.4238155, 173.5028053, 175.5954727,
    177.7018325, 179.8218996, 181.9556888, 184.1032148, 186.2644923, 188.4395359,
    190.6283601, 192.8309794, 195.0474081, 197.2776608, 199.5217516, 201.7796948,
    204.0515046, 206.337195, 208.6367802, 210.9502742, 213.2776909, 215.6190442,
    217.974348, 220.343616, 222.7268619, 225.1240995, 227.5353423, 229.960604,
    232.3998981, 234.8532379, 237.3206371, 239.8021088, 242.2976664, 244.8073232,
    247.3310924, 249.8689871, 252.4210206, 254.9872057, 257.5675556, 260.1620833,
    262.7708016, 265.3937234, 268.0308617, 270.682229, 273.3478383, 276.0277021,
    278.7218331, 281.430244, 284.1529473, 286.8899554, 289.641281, 292.4069364,
    295.1869339, 297.981286, 300.7900049, 303.6131029, 306.4505923, 309.3024851,
    312.1687935, 315.0495297, 317.9447056, 320.8543333, 323.7784247, 326.7169918,
    329.6700465, 332.6376007, 335.6196661, 338.6162545, 341.6273777, 344.6530474,
    347.6932753, 350.7480729, 353.8174518, 356.9014237, 360.0)

brightAnotherArrayCC5True = (0, 0x2E, 0x2E, 0x36, 0x30, 0x2A, 0x1F, 0x16, 0x0B,
    0, 0, 0x2D, 0x2E, 0x2A, 0x26, 0x21, 0x18, 0x0F, 0x0B, 0, 0, 0x29, 0x2A, 0x25,
    0x21, 0x1E, 0x16, 0x0F, 9, 0, 0, 0x23, 0x23, 0x20, 0x1B, 0x17, 0x11, 0x0B, 7, 0,
    0, 0x21, 0x21, 0x1D, 0x18, 0x14, 0x0F, 8, 6, 0, 0, 0x1F, 0x1E, 0x1B, 0x17, 0x13,
    0x0E, 8, 6, 0, 0, 0x19, 0x1B, 0x17, 0x13, 0x10, 0x0C, 7, 6, 0, 0, 0x19, 0x1A,
    0x17, 0x13, 0x10, 0x0C, 7, 6, 0, 0, 0x19, 0x18, 0x15, 0x12, 0x0F, 0x0C, 7, 6, 0,
    0, 0x17, 0x18, 0x14, 0x10, 0x0E, 0x0A, 6, 5, 0, 0, 0x17, 0x17, 0x13, 0x0F, 0x0D,
    9, 6, 5, 0, 0, 0x15, 0x15, 0x12, 0x0E, 0x0C, 9, 5, 5, 0, 0, 0x13, 0x14, 0x11,
    0x0D, 0x0B, 8, 5, 5, 0, 0, 0x13, 0x13, 0x10, 0x0D, 0x0B, 8, 5, 5, 0, 0, 0x12,
    0x13, 0x10, 0x0C, 0x0A, 7, 5, 5, 0, 0, 0x0E, 0x12, 0x0F, 0x0B, 0x0A, 7, 4, 5, 0,
    0, 0x0E, 0x11, 0x0E, 0x0A, 9, 6, 4, 5, 0, 0, 0x0D, 0x10, 0x0D, 0x0A, 8, 7, 4, 4,
    0, 0, 0x0D, 0x0F, 0x0C, 9, 7, 5, 4, 4, 0, 0, 0x0D, 0x0E, 0x0C, 9, 7, 5, 4, 4, 0,
    0, 0x0C, 0x0E, 0x0B, 8, 7, 5, 4, 4, 0, 0, 0x0B, 0x0E, 0x0B, 8, 7, 5, 3, 4, 0, 0,
    7, 0x0D, 0x0A, 7, 6, 5, 3, 4, 0, 0, 6, 0x0C, 9, 7, 6, 4, 2, 4, 0, 0, 6, 0x0C, 9,
    6, 5, 3, 2, 4, 0, 0, 6, 0x0B, 9, 6, 5, 3, 3, 4, 0, 0, 6, 0x0B, 8, 6, 5, 3, 3, 4,
    0, 0, 6, 0x0A, 8, 5, 4, 3, 3, 4, 0, 0, 6, 9, 7, 5, 4, 3, 3, 4, 0, 0, 6, 9, 7, 4,
    4, 3, 3, 4, 0, 0, 5, 8, 6, 4, 3, 3, 3, 4, 0, 0, 5, 8, 6, 3, 3, 2, 2, 4, 0, 0, 5,
    7, 5, 3, 3, 2, 2, 4, 0, 0, 5, 6, 5, 3, 3, 2, 2, 4, 0, 0, 5, 6, 5, 3, 2, 2, 2, 3,
    0, 0, 4, 5, 4, 2, 2, 2, 2, 3, 0, 0, 4, 5, 4, 2, 2, 0, 2, 3, 0, 0, 4, 5, 4, 2, 2,
    0, 0, 3, 0, 0, 4, 4, 3, 0, 0, 0, 0, 3, 0, 0, 3, 4, 3, 0, 0, 0, 0, 3, 0, 0, 3, 4,
    2, 2, 0, 0, 2, 0, 0, 0, 3, 4, 3, 2, 0, 2, 0, 0, 0, 0, 3, 3, 2, 0, 0, 0, 0, 0, 0,
    0, 3, 3, 2, 0, 0, 0, 2, 0, 0, 0, 2, 4, 2, 0, 0, 2, 3, 0, 0, 0, 2, 4, 2, 0, 0, 2,
    2, 0, 0, 0, 2, 4, 3, 0, 0, 3, 3, 0, 0, 0, 2, 3, 2, 0, 0, 2, 3, 0, 0, 0, 2, 3, 0,
    0, 0, 0, 3, 0, 0, 0, 2, 3, 2, 0, 0, 2, 4, 0, 0, 0, 2, 4, 2, 0, 0, 3, 0, 0, 0, 0,
    2, 2, 2, 0, 0, 0, 3, 1, 0, 0, 1, 3, 0, 0, 0, 0, 3, 0, 0, 0, 1, 2, 0, 0, 0, 0, 3,
    0, 0, 0, 1, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

brightAnotherArrayCC5False = (0, 0x37, 0x35, 0x32, 0x2E, 0x28, 0x1E, 0x12, 9,
    0, 0, 0x30, 0x2D, 0x29, 0x26, 0x1F, 0x18, 0x0F, 7, 0, 0, 0x2A, 0x28, 0x26, 0x21,
    0x1C, 0x15, 0x0E, 7, 0, 0, 0x28, 0x23, 0x20, 0x1B, 0x16, 0x12, 0x0C, 6, 0, 0,
    0x24, 0x20, 0x1E, 0x1A, 0x15, 0x10, 0x0A, 6, 0, 0, 0x20, 0x1D, 0x1B, 0x16, 0x10,
    0x0F, 9, 5, 0, 0, 0x1D, 0x1B, 0x19, 0x14, 0x0F, 0x0E, 8, 5, 0, 0, 0x1A, 0x19,
    0x18, 0x12, 0x0E, 0x0D, 7, 5, 0, 0, 0x18, 0x18, 0x15, 0x10, 0x0D, 0x0C, 6, 5, 0,
    0, 0x17, 0x17, 0x14, 0x10, 0x0C, 0x0B, 6, 5, 0, 0, 0x16, 0x16, 0x13, 0x0F, 0x0B,
    0x0A, 6, 5, 0, 0, 0x16, 0x15, 0x12, 0x0E, 0x0A, 9, 6, 4, 0, 0, 0x16, 0x14, 0x12,
    0x0E, 0x0A, 9, 5, 4, 0, 0, 0x16, 0x14, 0x10, 0x0D, 0x0A, 8, 5, 4, 0, 0, 0x16,
    0x13, 0x10, 0x0C, 9, 8, 5, 4, 0, 0, 0x15, 0x12, 0x0F, 0x0B, 8, 7, 5, 4, 0, 0,
    0x13, 0x11, 0x0D, 9, 7, 7, 5, 4, 0, 0, 0x13, 0x11, 0x0D, 9, 7, 7, 5, 4, 0, 0,
    0x12, 0x0F, 0x0C, 8, 6, 6, 4, 4, 0, 0, 0x12, 0x0F, 0x0C, 8, 6, 6, 4, 4, 0, 0,
    0x11, 0x0E, 0x0B, 8, 6, 5, 4, 4, 0, 0, 0x11, 0x0E, 0x0B, 8, 6, 4, 4, 4, 0, 0,
    0x10, 0x0E, 0x0B, 8, 5, 4, 4, 4, 0, 0, 0x0F, 0x0D, 0x0A, 7, 5, 4, 4, 4, 0, 0,
    0x0F, 0x0C, 0x0A, 7, 5, 4, 4, 4, 0, 0, 0x0E, 0x0C, 0x0A, 7, 5, 4, 3, 4, 0, 0,
    0x0E, 0x0B, 9, 7, 5, 4, 3, 4, 0, 0, 0x0E, 0x0B, 9, 7, 5, 4, 3, 4, 0, 0, 0x0E,
    0x0B, 9, 7, 5, 4, 3, 4, 0, 0, 0x0E, 0x0B, 9, 7, 5, 4, 3, 4, 0, 0, 0x0D, 0x0A, 9,
    6, 4, 4, 3, 4, 0, 0, 0x0D, 0x0A, 8, 6, 4, 4, 3, 4, 0, 0, 0x0C, 0x0A, 7, 6, 4, 4,
    3, 4, 0, 0, 0x0C, 0x0A, 7, 6, 4, 4, 3, 4, 0, 0, 0x0B, 9, 7, 5, 4, 4, 3, 4, 0, 0,
    0x0B, 9, 6, 5, 4, 4, 3, 4, 0, 0, 0x0B, 8, 6, 4, 4, 4, 3, 4, 0, 0, 9, 8, 6, 4, 4,
    4, 3, 4, 0, 0, 9, 8, 6, 4, 4, 4, 3, 4, 0, 0, 9, 8, 6, 4, 4, 4, 3, 4, 0, 0, 9, 8,
    6, 4, 4, 4, 3, 3, 0, 0, 9, 7, 5, 4, 4, 4, 3, 2, 0, 0, 9, 7, 5, 4, 4, 4, 3, 2, 0,
    0, 9, 7, 5, 4, 4, 4, 3, 1, 0, 0, 9, 7, 5, 4, 4, 4, 3, 1, 0, 0, 9, 7, 4, 4, 4, 4,
    3, 1, 0, 0, 8, 6, 4, 4, 4, 3, 2, 1, 0, 0, 8, 6, 4, 3, 4, 3, 2, 1, 0, 0, 8, 5, 4,
    3, 3, 3, 2, 1, 0, 0, 7, 5, 4, 3, 3, 3, 2, 1, 0, 0, 7, 5, 4, 3, 3, 3, 2, 1, 0, 0,
    7, 5, 4, 2, 3, 3, 2, 1, 0, 0, 7, 5, 3, 2, 2, 3, 2, 1, 0, 0, 6, 5, 3, 2, 1, 3, 2,
    1, 0, 0, 6, 4, 3, 1, 1, 3, 2, 1, 0, 0, 5, 3, 2, 1, 1, 2, 2, 1, 0, 0, 4, 3, 2, 1,
    0, 2, 2, 1, 0, 0, 4, 3, 1, 1, 0, 2, 2, 1, 0, 0, 4, 3, 1, 1, 0, 2, 2, 0, 0, 0, 3,
    3, 2, 1, 0, 1, 1, 0, 0, 0, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 0, 0, 0, 0, 0,
    0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

def __getIndexFromDoubleComparison(counterNr, doublesTable, isCC5True) :
    # Create a 0 filled table
    output = [0] * (10)

    # Compare each double
    counter = 9
    while counter > 0 :
        currentValue = doublesTable[counter]
        # Parse each value of the comparison table
        i = 0
        while i < 0x100 :
            compValue = brightComparisonValues[i]

            if compValue >= currentValue :
                # Stop here if it's the first element
                if i == 0 :
                    break

                tmpVal = currentValue - brightComparisonValues[i-1]
                compValue -= currentValue
                if tmpVal >= compValue :
                    break
                if compValue > tmpVal :
                    i -= 1
                    break

            i += 1

        if isCC5True :
            basePtr = brightAnotherArrayCC5True[counterNr*10 + counter]
        else :
            basePtr = brightAnotherArrayCC5False[counterNr*10 + counter]
        output[counter] = basePtr + i
        counter -= 1
    
    return output


def __getCorrespondingFractionalValues(indexTable, fractionalValues) :
    # Create a 0 filled table
    output = [0] * (10*3)

    for i in range(10) :
        index = indexTable[i]
        for j in range(3) :
            output[i*3 + j] = fractionalValues[index*3 + j] 

    return output

brightScalarVector3 = (0, 0x258, 0x40, 0x140, 0x40, 0x140, 0x40, 0x140, 0x40,
    0x140, 0x40, 0x140, 0x40, 0x140, 0x40, 0x140, 0x40, 0x140, 0x81, 0x280)

brightShiftFactorPerChannelCC5True = (0, 0, 0, 0, 0, 0, -4, 2, -2, -5, 0, -4,
    -3, 1, -2, -8, 3, -5, -0x0A, 4, -5, -6, 0, -4, -4, 0, -3, -0x0B, 1, -7, 0, 0, 0,
    0, 0, 0, -4, 2, -2, -5, 1, -4, -6, 1, -4, -0x0B, 3, -8, -0x0A, 2, -5, -6, 0, -4,
    -3, 0, -3, -7, 0, -3, 0, 0, 0, 0, 0, 0, -3, 2, -3, -6, 1, -4, -7, 2, -5, -0x0B,
    3, -8, -0x0A, 2, -5, -4, 0, -4, -3, 0, -3, -5, 0, -2, 0, 0, 0, 0, 0, 0, -4, 1,
    -4, -4, 1, -4, -8, 1, -5, -0x0A, 4, -7, -8, 3, -5, -3, 1, -3, -2, 1, -2, -4, 0,
    -2, 0, 0, 0, 0, 0, 0, -3, 1, -4, -6, 1, -4, -7, 1, -4, -0x0B, 3, -7, -8, 3, -5,
    -3, 1, -3, -1, 0, -1, -3, 0, -1, 0, 0, 0, 0, 0, 0, -3, 2, -4, -5, 1, -4, -7, 1,
    -4, -0x0A, 3, -6, -8, 3, -4, -3, 1, -3, -1, 0, -1, -3, 0, -1, 0, 0, 0, 0, 0, 0,
    -4, 1, -4, -5, 1, -4, -6, 1, -4, -0x0A, 3, -6, -7, 3, -4, -2, 1, -3, -1, 0, -1,
    -2, 0, -1, 0, 0, 0, 0, 0, 0, -6, 2, -4, -5, 1, -4, -6, 1, -4, -9, 3, -6, -7, 3,
    -4, -3, 1, -3, -1, 0, -1, -2, 0, -1, 0, 0, 0, 0, 0, 0, -5, 1, -4, -5, 2, -3, -8,
    1, -5, -9, 3, -5, -5, 3, -3, -2, 1, -2, -1, 0, -1, -2, 0, -1, 0, 0, 0, 0, 0, 0,
    -5, 1, -3, -7, 2, -5, -7, 2, -5, -9, 3, -6, -7, 1, -4, -2, 0, -2, 0, 0, -1, -2,
    0, -1, 0, 0, 0, 0, 0, 0, -5, 1, -3, -9, 2, -6, -6, 2, -5, -8, 3, -6, -7, 1, -4,
    -2, 0, -2, 0, 0, -1, -2, 0, -1, 0, 0, 0, 0, 0, 0, -6, 2, -5, -8, 2, -6, -6, 2,
    -5, -7, 2, -6, -6, 1, -3, -2, 0, -2, 0, 0, -1, -2, 0, -1, 0, 0, 0, 0, 0, 0, -6,
    2, -4, -8, 2, -6, -6, 2, -5, -7, 2, -6, -6, 1, -3, -2, 0, -2, 0, 0, -1, -2, 0,
    -1, 0, 0, 0, 0, 0, 0, -6, 2, -4, -8, 2, -6, -6, 2, -5, -7, 2, -5, -6, 1, -3, -2,
    0, -2, 0, 0, -1, -2, 0, -1, 0, 0, 0, 0, 0, 0, -6, 2, -4, -8, 2, -6, -6, 2, -5,
    -7, 2, -5, -6, 1, -3, -2, 0, -2, 0, 0, -1, -2, 0, -1, 0, 0, 0, 0, 0, 0, -6, 2,
    -4, -8, 2, -6, -6, 2, -5, -7, 2, -5, -5, 1, -3, -2, 0, -2, 0, 0, -1, -2, 0, -1,
    0, 0, 0, 0, 0, 0, -6, 3, -4, -8, 2, -5, -6, 2, -5, -7, 2, -4, -5, 1, -3, -2, 0,
    -2, 0, 0, -1, -2, 0, -1, 0, 0, 0, 0, 0, 0, -6, 2, -4, -7, 2, -5, -5, 2, -4, -5,
    2, -3, -2, 1, -1, -2, 0, -1, -2, 0, -1, -2, 0, -1, 0, 0, 0, 0, 0, 0, -8, 2, -5,
    -7, 2, -5, -6, 2, -4, -5, 2, -4, -4, 1, -2, -2, 0, -2, 0, 0, -1, 0, 0, 1, 0, 0,
    0, 0, 0, 0, -7, 3, -5, -6, 2, -4, -6, 2, -4, -5, 2, -4, -4, 1, -2, -2, 0, -2, 0,
    0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, -6, 2, -5, -9, 3, -6, -6, 2, -4, -5, 2, -4,
    -4, 1, -2, -1, 0, -2, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, -6, 3, -5, -9, 2, -6,
    -5, 2, -4, -5, 1, -4, -4, 1, -2, -1, 0, -2, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0,
    -7, 2, -5, -9, 2, -6, -5, 2, -4, -5, 1, -4, -4, 1, -2, -1, 0, -2, 0, 0, -1, 0,
    0, 1, 0, 0, 0, 0, 0, 0, -7, 1, -5, -9, 2, -6, -5, 2, -4, -4, 1, -4, -4, 0, -2,
    -1, 0, -2, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, -7, 2, -5, -8, 2, -5, -5, 2, -4,
    -4, 1, -3, -4, 0, -2, -1, 0, -2, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, -7, 2, -5,
    -7, 2, -5, -5, 2, -4, -4, 1, -3, -4, 0, -2, 0, 0, -2, 0, 0, -1, 0, 0, 1, 0, 0,
    0, 0, 0, 0, -7, 1, -6, -8, 3, -5, -5, 1, -4, -4, 1, -3, -4, 0, -2, 0, 0, -2, 0,
    0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, -8, 2, -6, -6, 2, -5, -4, 1, -3, -4, 1, -3,
    -4, 0, -2, 0, 0, -2, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, -0x0B, 2, -7, -5, 2,
    -4, -4, 1, -4, -3, 1, -2, -4, 0, -2, 0, 0, -2, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0,
    0, -0x0B, 2, -7, -6, 2, -4, -5, 1, -4, -3, 1, -3, -2, 0, -1, 0, 0, -2, 0, 0, -1,
    0, 0, 1, 0, 0, 0, 0, 0, 0, -0x0B, 2, -6, -5, 2, -4, -6, 1, -4, -2, 1, -2, -2, 0,
    -1, 0, 0, -2, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, -0x0B, 3, -6, -4, 1, -3, -5,
    1, -3, -2, 1, -2, -1, 0, -1, 0, 0, -2, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0,
    -0x0B, 3, -6, -5, 1, -3, -4, 1, -3, -2, 1, -2, -1, 0, -1, 0, 0, -2, 0, 0, -1, 0,
    0, 1, 0, 0, 0, 0, 0, 0, -0x0B, 2, -5, -4, 1, -3, -3, 1, -2, -2, 1, -2, -1, 0,
    -1, 0, 0, -2, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, -0x0B, 2, -5, -3, 1, -2, -4,
    1, -3, -2, 0, -2, -1, 0, -1, 0, 0, -2, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0,
    -0x0B, 2, -5, -3, 1, -2, -4, 1, -2, -2, 0, -2, -1, 0, -1, 0, 0, -2, 0, 0, -1, 0,
    0, 1, 0, 0, 0, 0, 0, 0, -0x0B, 2, -4, -4, 1, -3, -4, 1, -2, -1, 0, -2, -1, 0,
    -1, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, -0x0B, 2, -5, -4, 0, -2, -3,
    1, -2, -1, 0, -2, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, -0x0C,
    2, -5, -3, 0, -2, -2, 1, -2, -1, 0, -1, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0,
    0, 0, 0, 0, 0, -0x0C, 2, -5, -3, 0, -2, -2, 1, -2, -1, 0, -1, -1, 0, 0, 0, 0,
    -1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, -0x0C, 2, -6, -3, 0, -2, -2, 1, -2, -1,
    0, -1, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, -0x0C, 2, -6, -3,
    0, -2, -2, 1, -2, -1, 0, -1, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 0, -0x0C, 2, -6, -3, 0, -2, -2, 1, -2, -1, 0, -1, -1, 0, 0, 0, 0, -1, 0, 0,
    0, 0, 0, 1, 0, 0, 0, 0, 0, 0, -0x0A, 3, -6, -4, 0, -3, -1, 0, -1, 1, 1, -1, -1,
    0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, -0x0A, 2, -6, -2, 0, -2, -1,
    0, -2, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0x0A,
    2, -6, -2, 0, -2, -1, 0, -2, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, -0x0A, 2, -6, -2, 0, -2, -1, 0, -2, -1, 0, -1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -9, 2, -6, -2, 0, -2, -1, 0, -2, -1, 0, -1,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -9, 2, -6, -2, 0, -2, -1,
    0, -2, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -9, 2,
    -6, -2, 0, -2, -1, 0, -2, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, -9, 2, -6, -2, 0, -1, -1, 0, -2, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -9, 2, -6, 0, 1, -1, -1, 0, -1, -2, 0, -1, 0, 0,
    -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -7, 1, -4, -3, 0, -2, -1, 0,
    -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -7, 2, -4,
    -3, 0, -2, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, -7, 1, -4, -2, 0, -1, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, -6, 1, -3, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -6, 1, -4, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -6, 1, -4, -1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

brightShiftFactorPerChannelCC5False = ( 0, 0, 0, 0, 0, 0, -6, 1, -1, -4, 1,
    -2, -7, 2, -3, -0x0D, 3, -8, -0x0D, 0, -9, -6, 0, -4, -4, 0, -2, -0x0D, 1, -7,
    0, 0, 0, 0, 0, 0, -6, 1, -2, -6, 1, -4, -0x0B, 1, -5, -0x10, 2, -8, -0x0D, 0,
    -8, -5, 0, -4, -4, 0, -2, -9, 1, -5, 0, 0, 0, 0, 0, 0, -7, 1, -4, -7, 1, -4,
    -0x0B, 1, -5, -0x10, 2, -9, -0x0C, 0, -8, -5, 0, -4, -4, 0, -2, -8, 0, -5, 0, 0,
    0, 0, 0, 0, -7, 1, -4, -8, 1, -4, -0x0B, 1, -5, -0x0F, 3, -8, -0x0B, 0, -6, -5,
    0, -3, -4, 0, -2, -6, 0, -4, 0, 0, 0, 0, 0, 0, -7, 1, -4, -8, 1, -4, -0x0B, 3,
    -5, -0x0E, 3, -8, -0x0A, 0, -6, -5, 0, -3, -4, 0, -2, -5, 0, -3, 0, 0, 0, 0, 0,
    0, -7, 1, -4, -8, 1, -4, -0x0B, 2, -5, -0x0E, 4, -6, -9, 0, -5, -4, 0, -2, -3,
    0, -2, -5, 0, -3, 0, 0, 0, 0, 0, 0, -7, 1, -4, -8, 1, -4, -0x0C, 3, -5, -0x0D,
    4, -6, -9, 0, -5, -4, 0, -2, -2, 0, -2, -4, 0, -2, 0, 0, 0, 0, 0, 0, -7, 1, -4,
    -8, 1, -5, -0x0C, 3, -5, -0x0C, 4, -6, -9, 0, -5, -4, 0, -2, -2, 0, -2, -4, 0,
    -2, 0, 0, 0, 0, 0, 0, -7, 1, -4, -9, 1, -5, -0x0C, 3, -5, -0x0B, 4, -6, -8, 0,
    -3, -3, 0, -1, -2, 0, -2, -4, 0, -2, 0, 0, 0, 0, 0, 0, -7, 1, -5, -9, 1, -6,
    -0x0B, 3, -6, -0x0B, 4, -6, -8, 0, -3, -3, 0, -1, -2, 0, -2, -4, 0, -2, 0, 0, 0,
    0, 0, 0, -8, 0, -5, -9, 1, -6, -0x0B, 3, -6, -0x0B, 4, -6, -8, 0, -3, -2, 0, -1,
    -2, 0, -2, -3, 0, -2, 0, 0, 0, 0, 0, 0, -8, 0, -5, -0x0B, 1, -6, -0x0A, 3, -5,
    -0x0B, 4, -6, -7, 0, -3, -2, 0, -1, -2, 0, -2, -3, 0, -1, 0, 0, 0, 0, 0, 0, -8,
    0, -5, -0x0B, 0, -6, -0x0A, 3, -5, -0x0A, 4, -6, -7, 0, -3, -2, 0, -1, -2, 0,
    -1, -2, 0, -1, 0, 0, 0, 0, 0, 0, -9, 0, -5, -0x0B, 0, -6, -9, 3, -5, -0x0A, 3,
    -6, -6, 0, -3, -2, 0, -1, -2, 0, -1, -2, 0, -1, 0, 0, 0, 0, 0, 0, -9, 0, -5,
    -0x0B, 0, -6, -9, 3, -5, -9, 3, -5, -6, 0, -3, -2, 0, -1, -2, 0, -1, -2, 0, -1,
    0, 0, 0, 0, 0, 0, -0x0A, 0, -5, -0x0B, 0, -7, -9, 3, -5, -8, 4, -5, -5, 0, -2,
    -2, 0, 0, -2, 0, -1, -2, 0, -1, 0, 0, 0, 0, 0, 0, -0x0B, 0, -5, -0x0B, 0, -7,
    -9, 4, -5, -7, 4, -4, -4, 0, -1, -2, 0, 0, -1, 0, -1, -2, 0, -1, 0, 0, 0, 0, 0,
    0, -0x0C, 0, -5, -0x0B, 0, -7, -9, 4, -5, -7, 4, -4, -3, 0, -1, -2, 0, 0, -1, 0,
    -1, -2, 0, -1, 0, 0, 0, 0, 0, 0, -0x0B, 1, -5, -0x0A, 0, -7, -8, 4, -5, -6, 4,
    -4, -3, 0, -1, -2, 0, 0, -2, 0, -1, -2, 0, -1, 0, 0, 0, 0, 0, 0, -0x0B, 1, -5,
    -0x0A, 0, -8, -7, 4, -5, -6, 4, -4, -3, 0, -1, -2, 0, 0, -2, 0, -1, -2, 0, -1,
    0, 0, 0, 0, 0, 0, -0x0B, 1, -5, -0x0B, 0, -8, -7, 4, -5, -6, 3, -4, -3, 0, -1,
    -2, 0, 0, -2, 0, -1, -1, 0, -1, 0, 0, 0, 0, 0, 0, -0x0B, 1, -5, -0x0B, 0, -8,
    -6, 4, -5, -7, 2, -4, -3, 0, 0, -2, 0, 0, -2, 0, -1, -1, 0, -1, 0, 0, 0, 0, 0,
    0, -0x0A, 1, -5, -0x0B, 0, -8, -7, 3, -5, -6, 2, -4, -3, 0, 0, -2, 0, 0, -2, 0,
    -1, -1, 0, -1, 0, 0, 0, 0, 0, 0, -8, 1, -5, -0x0B, 0, -8, -6, 3, -5, -6, 2, -4,
    -3, 0, 0, -2, 0, 0, -1, 0, -1, -1, 0, -1, 0, 0, 0, 0, 0, 0, -7, 2, -5, -0x0A, 1,
    -8, -6, 4, -5, -6, 2, -3, -3, 0, 0, -2, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0,
    0, -6, 2, -5, -0x0B, 0, -8, -6, 4, -5, -5, 2, -3, -3, 0, 0, -2, 0, 0, -1, 0, -1,
    0, 0, 0, 0, 0, 0, 0, 0, 0, -6, 3, -5, -0x0C, 1, -8, -6, 3, -5, -5, 2, -3, -2, 0,
    0, -1, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -7, 3, -5, -0x0B, 1, -8, -5,
    2, -5, -5, 2, -3, -2, 0, 0, -1, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -7,
    3, -5, -0x0B, 1, -8, -5, 2, -4, -6, 2, -3, -2, 0, 0, -1, 0, 0, -1, 0, -1, 0, 0,
    0, 0, 0, 0, 0, 0, 0, -7, 3, -5, -0x0B, 1, -0x0A, -5, 2, -4, -6, 1, -3, -2, 0,
    -2, -1, 0, 0, -1, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, -7, 3, -5, -0x0A, 0, -0x0A,
    -5, 2, -4, -6, 1, -3, -2, 0, -1, -1, 0, 0, -1, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0,
    0, -7, 3, -5, -9, 0, -0x0A, -5, 2, -4, -6, 1, -3, -2, 0, -1, -1, 0, 0, -1, 0,
    -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, -7, 3, -5, -9, 0, -0x0A, -4, 2, -3, -6, 1, -3,
    -2, 0, -1, -1, 0, 0, -1, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, -7, 3, -5, -8, 0,
    -0x0A, -4, 2, -3, -6, 1, -3, -2, 0, -2, -1, 0, 0, -1, 0, -1, 0, 0, -1, 0, 0, 0,
    0, 0, 0, -7, 3, -5, -8, 0, -0x0A, -4, 2, -3, -5, 0, -3, -2, 0, -2, -1, 0, 0, -1,
    0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, -8, 3, -6, -8, 0, -9, -4, 2, -3, -4, 0, -3,
    -1, 0, -2, 0, 0, 0, -1, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, -8, 3, -6, -7, 0, -7,
    -4, 2, -3, -4, 0, -3, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0,
    -8, 3, -7, -6, 0, -6, -4, 2, -3, -3, 0, -3, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0,
    -2, 0, 0, 0, 0, 0, 0, -8, 3, -8, -5, 1, -6, -4, 2, -3, -2, 0, -3, -1, 0, -1, 0,
    0, 0, -1, 0, -1, 0, 0, -2, 0, 0, 0, 0, 0, 0, -8, 3, -8, -5, 1, -6, -4, 2, -3,
    -2, 0, -3, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, -2, 0, 0, 0, 0, 0, 0, -8, 3, -8,
    -6, 1, -6, -4, 1, -4, -2, 0, -3, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, -2, 0, 0,
    0, 0, 0, 0, -8, 3, -8, -6, 2, -6, -4, 1, -4, -2, 0, -2, -1, 0, -1, 0, 0, 0, 0,
    0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, -8, 3, -8, -6, 2, -5, -4, 1, -3, -2, 0, -2,
    -1, 0, -1, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, -8, 3, -8, -6, 2, -5,
    -4, 1, -3, -2, 0, -2, -1, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0,
    -8, 3, -8, -6, 2, -5, -4, 1, -3, -2, 0, -2, -1, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0,
    -1, 0, 0, 0, 0, 0, 0, -8, 3, -8, -6, 1, -5, -3, 1, -3, -2, 0, -2, -1, 0, -1, 0,
    0, -1, 0, 0, -1, 0, 0, -2, 0, 0, 0, 0, 0, 0, -8, 3, -8, -5, 2, -4, -3, 1, -3,
    -2, 0, -2, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -0x0A, 3,
    -0x0A, -5, 1, -5, -3, 1, -3, -2, 0, -2, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0,
    0, 0, 0, 0, 0, -0x0A, 3, -9, -5, 1, -5, -2, 1, -3, -1, 0, -2, 0, 0, -1, 0, 0, 0,
    0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -9, 3, -8, -6, 1, -5, -2, 1, -3, -1, 0, -2,
    0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -9, 3, -9, -5, 0, -4,
    -2, 1, -2, -1, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0,
    -8, 3, -8, -5, 0, -4, -2, 1, -2, -1, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0,
    -1, 0, 0, 0, 0, 0, 0, -8, 3, -8, -4, 1, -4, -2, 0, -2, -1, 0, -1, 0, 0, -1, 0,
    0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -7, 2, -7, -4, 1, -4, -2, 0, -2, -1,
    0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -6, 2, -5, -4, 1,
    -3, -2, 0, -2, -1, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0,
    0, -6, 2, -5, -3, 1, -2, -1, 0, -2, -1, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0,
    -1, 0, 0, 0, 0, 0, 0, -6, 2, -4, -2, 1, -2, -1, 0, -2, 0, 0, -1, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -4, 1, -4, -2, 1, -2, -1, 0, -2, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

def __s(counterNr, tempFractionalValues, reordered340, isCC5True) :
    # Create a 0 filled table
    output = [0] * (10*3)

    counter = 9
    while counter > 0 :
        factorA = brightScalarVector3[counter*2]
        factorB = brightScalarVector3[counter*2 + 1]

        for i in range(3) :
            if counter == 1 :
                xmm1 = 7.2 - tempFractionalValues[2*3 + i]
                xmm2 = 7.2 - tempFractionalValues[1*3 + i]
            elif counter == 9 :
                xmm1 = 7.2 - 1.5
                xmm2 = 7.2 - tempFractionalValues[9*3 + i]
            else :
                xmm1 = tempFractionalValues[i] - tempFractionalValues[(counter+1) * 3 + i]
                xmm2 = tempFractionalValues[i] - tempFractionalValues[counter * 3 + i]

            val = int(((factorB * xmm2) / xmm1) - factorA + 0.0005)
            if isCC5True :
                val += brightShiftFactorPerChannelCC5True[counterNr*10*3 + (counter * 3) + i]
            else :
                val += brightShiftFactorPerChannelCC5False[counterNr*10*3 + (counter * 3) + i]

            if val < 0 :
                val = 0
            if val > 0xFF and counter != 9 :
                val = 0xFF
            output[(counter * 3) + i] = val

        counter -= 1

    # Init the first line of the table
    for i in range(3) :
        output[i] = reordered340[i]

    return output
                
def toByte(v) :
    if v > 0xFF :
        return v & 0xFF
    return v

def initBrightnessTable384(aux, displayInfo, cc5State) :
    output = [0] * (3*11*0x42)

    reordered340 = __reorderTable340(displayInfo['table340'])
    scaleFactor = __computeScaleFactorFromVectorized340(reordered340)
    fractionalValues = __computeFractionalValueTable(scaleFactor)
    tempFinal = [0] * 0x42
    for i in range(0x42) :
        temp10Double = __computeTemp10DoubleTable(i, cc5State)
        temp10DWordAsIndex = __getIndexFromDoubleComparison(i, temp10Double, cc5State)
        tempFractionalValues = __getCorrespondingFractionalValues(
            temp10DWordAsIndex, fractionalValues)
        tempFinal[i] = __s(i, tempFractionalValues, reordered340, cc5State)
    
    # Reorder the result
    for i in range(0x42) :
        ptr = 11*3*i
        for j in range(3) :
            for k in range(8) :
                output[ptr] = toByte(tempFinal[i][(k+2) * 3 + j])
                ptr += 1
            output[ptr] = toByte(tempFinal[i][1*3 + j])
            output[ptr+1] = int(tempFinal[i][9*3 + j] / 2) & 0x80
            output[ptr+2] = toByte(tempFinal[i][j])
            ptr += 3

    # Save the table
    displayInfo['table384'] = output


def initBrightnessTable363(aux, displayInfo) :
    result = []
    for (valA, valB, valC) in registerValuesB :
        result.append(readDisplayRegister2(aux, valA, valB, valC))
    displayInfo['table363'] = result


def adjustColorProfile(displayInfo) :
    tmp=[0,0,0,0]
    v4 = displayInfo['reg_27'] | (displayInfo['reg_26'] << 8)
    v8 = (displayInfo['reg_29'] | (displayInfo['reg_28'] << 8)) << 10
    tmp[0] = int(v8 - (44032 * v4) / 40 + 46080) >> 10
    tmp[1] = int(v8 - (317440 * v4) / 297 - 3072) >> 10
    tmp[2] = int((375808 * v4) / 84 + v8 - 16696320) >> 10
    tmp[3] = int((340992 * v4) / 107 + v8 - 12693504) >> 10

    if (tmp[0] <= 0) :
        if (tmp[1] >= 0) :
            if (tmp[2] > 0) :
                ptr = 6
            else :
                ptr = (tmp[3] >> 31) + 5
        else :
            if (tmp[2] > 0) :
                ptr = 9
            else :
                ptr = (tmp[3] >> 31) + 8
    else :
        if (tmp[2] > 0) :
            ptr = 3
        else :
            ptr = (tmp[3] >> 31) + 2
    if (ptr - 1) > 8 :
        ptr = 1

    adjA1 = colorProfileAdjTableA[3 * ptr]
    adjA2 = colorProfileAdjTableA[3 * ptr + 1]
    adjA3 = colorProfileAdjTableA[3 * ptr + 2]
    adjB1 = colorProfileAdjTableB[3 * ptr]
    adjB2 = colorProfileAdjTableB[3 * ptr + 1]
    adjB3 = colorProfileAdjTableB[3 * ptr + 2]
    
    colorProfile0[0x67] = adjB1
    colorProfile0[0x69] = adjB2
    colorProfile0[0x6B] = adjB3
    colorProfile1[0x67] = adjA1
    colorProfile1[0x69] = adjA2
    colorProfile1[0x6B] = adjA3
    colorProfile2[0x67] = adjB1
    colorProfile2[0x69] = adjB2
    colorProfile2[0x6B] = adjB3
    colorProfile3[0x67] = adjA1
    colorProfile3[0x69] = adjA2
    colorProfile3[0x6B] = adjA3
    colorProfile4[0x67] = adjA1
    colorProfile4[0x69] = adjA2
    colorProfile4[0x6B] = adjA3


sendDataM = (
    (0x491, [0x0F, 0xFF, 0x2]),
    (0x492, [0x30, 0x8A]),
    (0x492, [0x33, 0x08]),
    (0x491, [0x02, 0x7F, 0x1]),
    (0x491, [0x07, 0xFF, 0x4]),
)

def setBrightness(aux, displayInfo, isCC5True, brightness) :
    if brightness > 0x65 :
        return

    # Prepare data to send
    sendDataA[2][1][1] = structA[brightness]

    sendDataB[1][1][2] = structB[brightness][0]
    sendDataB[2][1][1] = structB[brightness][1]
    sendDataB[3][1][1] = structB[brightness][2]
    sendDataB[4][1][1] = structB[brightness][3]
    sendDataB[5][1][1] = structB[brightness][4]
    sendDataB[6][1][1] = structB[brightness][5]
    sendDataB[7][1][1] = structB[brightness][6]
    sendDataB[8][1][1] = structB[brightness][7]
    sendDataB[9][1][1] = structB[brightness][8]

    table384 = displayInfo['table384']
    ptr = ptrInto384Table[brightness] * 0x21
    for i in range(33) :
        sendDataD[i][1][1] = table384[ptr+i]

    # Send data
    if isCC5True :
        sendDataC[1][1][1] = structC[brightness][0]
        sendDataC[2][1][1] = structC[brightness][1]
        sendDataC[4][1][1] = structC2[ptrInto384Table[brightness]]
        sendDataC[5][1][1] = displayInfo['reg2_26']
        sendDataC[6][1][2] = 0x80 if brightness >= 0x64 else 0x90 # XXX
        aux.writeArray(sendDataC)

    else :
        isCAATrue = True
        if isCAATrue == False :
            sendDataM[2][1][1] = displayInfo['reg2_26']           
            aux.writeArray(sendDataM)
            sleep(0.001)
            aux.writeArray(sendDataE)
        sendDataC_cc5False[1][1][1] = structC_cc5False[brightness][0]
        sendDataC_cc5False[2][1][1] = structC_cc5False[brightness][1]
        sendDataC_cc5False[3][1][2] = 0x80 if brightness >= 0x64 else 0x90 # XXX
        aux.writeArray(sendDataC_cc5False)
    
    # Send last data
    aux.writeArray(sendDataD)
    sleep(0.001)
    aux.writeArray(sendDataE)
    aux.writeArray(sendDataA)
    aux.writeArray(sendDataB)

def applyColorProfile(aux, displayInfo, colorProfile) :
    if colorProfile == 0 :
        table = colorProfile0
    elif colorProfile == 1 :
        table = colorProfile1
    elif colorProfile == 2 :
        table = colorProfile2
    elif colorProfile == 3 :
        table = colorProfile3
    elif colorProfile == 4 :
        table = colorProfile4
    elif colorProfile == 5 :
        table = colorProfile5
    elif colorProfile == 6 :
        table = colorProfile6
    else :
        table = colorProfile3

    i = 0 
    for val in table :
        if i == 0 :
            sendDataColorProfile[i][1][2] = val
        else :
            sendDataColorProfile[i][1][1] = val
        i += 1

    aux.writeArray(sendDataColorProfile)


LOCK = threading.Lock()
def handler(aux, displayInfo, cc5State, maxBrightness):
    if not LOCK.acquire(blocking=False) :
        return

    try :
        with open(BRIGHTNESS_PATH) as infile:
            brightness = int(infile.readline())
            infile.close()
            aux.reopen()
            sendParaAux(aux)
            setBrightness(aux, displayInfo, cc5State, int(brightness * 101 / maxBrightness))
    except Exception as e:
        print('exception: %s' % e)
    finally:
        LOCK.release()


def watch(aux, displayInfo, cc5State) :
    with open(MAX_BRIGHTNESS_PATH) as infile:
        maxBrightness = int(infile.readline())
        infile.close()
    handler(aux, displayInfo, cc5State, maxBrightness)
    signal.signal(signal.SIGIO, lambda a, b: handler(aux, displayInfo, cc5State, maxBrightness))
    fd = os.open(BACKLIGHT_PATH, os.O_RDONLY)
    fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
    fcntl.fcntl(fd, fcntl.F_NOTIFY, fcntl.DN_MODIFY| fcntl.DN_MULTISHOT)
    lastTS = time()
    while True:
        sleep(2)
        newTS = time()
        if (newTS - lastTS > 4) :
            handler(aux, displayInfo, cc5State, maxBrightness)
        lastTS = newTS






colorProfile = 3
cc5State = True
aux = DPAux()
aux.open()
sendParaAux(aux)
getDisplayRegisters(aux, displayInfo)
getDisplayRegisters2(aux, displayInfo)
adjustColorProfile(displayInfo)
initBrightnessTable340(aux, displayInfo)
initBrightnessTable384(aux, displayInfo, cc5State)
initBrightnessTable363(aux, displayInfo)

if len(sys.argv) >= 2 :
    if sys.argv[1] == 'watch' :
        watch(aux, displayInfo, cc5State)
        sys.exit(0)
    brightness = int(sys.argv[1])
    if len(sys.argv) >= 3 :
        colorProfile = int(sys.argv[2])
else :
    print('Usage: %s <brightness level|watch> [<color profile>]' % sys.argv[0])
    print('    brightness level: value from 1 to 101')
    print('    watch: listening from sys brightness updates and adjust brightness accordingly')
    print('    color profile: value from 0 to 6 [3 by default]')
    sys.exit(0)
setBrightness(aux, displayInfo, cc5State, brightness)
applyColorProfile(aux, displayInfo, colorProfile)
aux.writeArray(sendDataColorProfile)

