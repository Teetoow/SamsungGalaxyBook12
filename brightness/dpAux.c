/*
 *      tables.c                (C) 2022-2023, Aurélien Croc (AP²C)
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
#include <unistd.h>
#include <fcntl.h>
#include "dpAux.h"



aux_t dpAuxOpen(const char *path)
{
    int fd;
   
    if ((fd = open(path, O_RDWR)) == -1)
        return 0;
    return fd;
}

char dpAuxRead(aux_t aux, int addr)
{
    char res;

    lseek(aux, addr, SEEK_SET);
    read(aux, &res, 1);
    return res;
}

void dpAuxWrite(aux_t aux, int addr, char val)
{
    lseek(aux, addr, SEEK_SET);
    write(aux, &val, 1);
}

void dpAuxWrites(aux_t aux, dpWrite_t data[])
{
    for (int i=0; data[i].addr; i++) {
        lseek(aux, data[i].addr, SEEK_SET);
        write(aux, data[i].val, data[i].nVal);
    }
}

void dpAuxClose(aux_t aux)
{
    close(aux);
}



/* vim: set expandtab tabstop=4 shiftwidth=4 smarttab tw=80 cin fenc=utf8 : */

