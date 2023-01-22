/*
 *      dpAux.h                 (C) 2022-2023, Aurélien Croc (AP²C)
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
#ifndef DPAUX_H
#define DPAUX_H

typedef int aux_t;


typedef struct {
    int             addr;
    int             nVal;
    char            val[3];
} dpWrite_t;

extern aux_t dpAuxOpen(const char *path);
extern char dpAuxRead(aux_t aux, int addr);
extern void dpAuxWrite(aux_t aux, int addr, char val);
//extern void dpAuxWrites(aux_t aux, int addr, int nVal, char *val);
extern void dpAuxWrites(aux_t aux, dpWrite_t data[]);
extern void dpAuxClose(aux_t aux);



#endif /* DPAUX_H */

/* vim: set expandtab tabstop=4 shiftwidth=4 smarttab tw=80 cin fenc=utf8 : */

