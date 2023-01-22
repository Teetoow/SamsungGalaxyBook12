/*
 *      brightness.h            (C) 2022-2023, Aurélien Croc (AP²C)
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
#ifndef BRIGHTNESS_H
#define BRIGHTNESS_H

#include "dpAux.h"

typedef struct {
    char                        reg2_26;
    char                        channelAdjustment[0x42][11 * 3];
    int                         highBrightnessMode;
    int                         lowBrightnessMode2;
} displayBrightness_t;


extern int accessParaAuxRegs(aux_t aux);
extern displayBrightness_t* initBrightness(aux_t aux, int colorProfile);
extern void setBrightness(aux_t aux, displayBrightness_t *dp, char brightness);
extern void setColorProfile(aux_t aux, displayBrightness_t *dp, char colorProfileNr);


#endif /* BRIGHTNESS_H */

/* vim: set expandtab tabstop=4 shiftwidth=4 smarttab tw=80 cin fenc=utf8 : */

