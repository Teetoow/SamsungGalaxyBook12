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
#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <fcntl.h>
#include <stdio.h>
#include <time.h>
#include "brightness.h"
#include "dpAux.h"

#define AUX_PATH "/dev/drm_dp_aux0"
#define BACKLIGHT_PATH "/sys/class/backlight/intel_backlight"
#define BRIGHTNESS_PATH BACKLIGHT_PATH "/brightness"
#define MAX_BRIGHTNESS_PATH BACKLIGHT_PATH "/max_brightness"

struct {
    pthread_mutex_t         lock;
    displayBrightness_t*    dp;
    aux_t                   aux;
    int                     maxBrightness;
} sigData;

/*
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
*/

void sigIOHandler(int)
{
    FILE *handle;

    // Try to get the mutex
    if (pthread_mutex_trylock(&sigData.lock) != 0)
        return;

    // Get the current brightness
    if ((handle = fopen(BRIGHTNESS_PATH, "r")) != NULL) {
        char buffer[256];
        int brightness;

        // Read the current brightness
        fgets((char *)&buffer, sizeof(buffer), handle);
        fclose(handle);
        brightness = strtol((char *)&buffer, (char **)NULL, 10);

        // Reopen the AUX device (in case of leaving power sleep mode)
        dpAuxClose(sigData.aux);
        sigData.aux = dpAuxOpen(AUX_PATH);
        accessParaAuxRegs(sigData.aux);

        // Set the new brightness
        setBrightness(sigData.aux, sigData.dp, 
            brightness * 101 / sigData.maxBrightness);
    }
    pthread_mutex_unlock(&sigData.lock);
}

void watch(aux_t aux, displayBrightness_t *dp, int colorProfile)
{
    int fd, maxBrightness;
    time_t lastTS, newTS;
    char buffer[256];
    size_t size;
    FILE *handle;

    // Get the maximum brightness value
    if ((handle = fopen(MAX_BRIGHTNESS_PATH, "r")) == NULL) {
        fprintf(stderr, "Error while opening " MAX_BRIGHTNESS_PATH "\n");
        return;
    }
    fgets((char *)&buffer, sizeof(buffer), handle);
    fclose(handle);

    // Prepare the signal data
    pthread_mutex_init(&sigData.lock, NULL);
    sigData.dp = dp;
    sigData.aux = aux;
    sigData.maxBrightness = strtol((char *)&buffer, (char **)NULL, 10);

    // Set the signal handler
    signal(SIGIO, sigIOHandler);

    // Set the brightness
    sigIOHandler(0);
    setColorProfile(aux, dp, colorProfile);

    // Open the /sys brightness directory in order to check changes
    if ((fd = open(BACKLIGHT_PATH, O_RDONLY)) == -1) {
        fprintf(stderr, "Error while opening path " BACKLIGHT_PATH "\n");
        return;
    }
    fcntl(fd, F_SETSIG, 0); 
    if (fcntl(fd, F_NOTIFY, DN_MODIFY | DN_MULTISHOT) == -1) {
        fprintf(stderr, "Cannot watch for changes on path " BACKLIGHT_PATH 
            "\n");
        return;
    }

    lastTS = time(NULL);
    while (1) {
        sleep(2);
        newTS = time(NULL);
        /*
         * This hacks in order to set back the previous brightness configuration
         * after the computer come back from power sleep state.
         */
        if (newTS - lastTS > 4) {
            // Reset the current brightness
            sigIOHandler(0);
            // Reset the current color profile
            setColorProfile(aux, dp, colorProfile);
        }
        lastTS = newTS;
    }
}

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
    if (!(aux = dpAuxOpen(AUX_PATH))) {
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
        watch(aux, dp, colorProfile);
        free(dp);
        dpAuxClose(aux);
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

