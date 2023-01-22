/*
 *      main.c                  (C) 2022-2023, Aurélien Croc (AP²C)
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
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "brightness.h"
#include "dpAux.h"



int main(int argc, char** argv)
{
    int brightness, colorProfile=3;
    displayBrightness_t* dp;
    aux_t aux;

    // Check arguments
    if (argc < 2) {
        printf("Usage: %s watch | <brightness> [<color profile>]\n", argv[0]);
        printf("     watch: listening for sys brightness changes and update "
            "the screen brightness accordingly\n");
        printf("     brightness: the brightness value between 1 and 101\n");
        printf("     color profile: the color profile to use between 0 and 6 "
            "[3 by default]\n");
        return 0;
    }
    
    // Open the DP AUX channel
    if (!(aux = dpAuxOpen("/dev/drm_dp_aux0"))) {
        fprintf(stderr, "Cannot open DP AUX device\n");
        return 1;
    }

    if (!(dp = initBrightness(aux, colorProfile))) {
        fprintf(stderr, "Cannot initialize the display\n");
        return 2;
    }

    // Extract the color profile
    if (argc == 3)
        colorProfile = strtol(argv[2], (char **)NULL, 10);

    // Check whether the program has to watch for brightness update
    if (!strcmp(argv[1], "watch")) {
        return 0;
    }

    // Otherwise set the brightness
    brightness = strtol(argv[1], (char **)NULL, 10);
    setColorProfile(aux, dp, colorProfile);
    setBrightness(aux, dp, brightness);


    free(dp);
    dpAuxClose(aux);

    return 0;
}


/* vim: set expandtab tabstop=4 shiftwidth=4 smarttab tw=80 cin fenc=utf8 : */

