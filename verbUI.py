#
#    verbUI.py                 (C) 2022-2023, Aurélien Croc (AP²C)
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

import subprocess

def execVerb(nid, verb, param) :
    nid = '0x%x' % nid
    verb = '0x%x' % verb
    param = '0x%x' % param
    output = subprocess.run(['hda-verb','/dev/snd/hwC0D0', nid, verb, param],capture_output=True).stdout.decode('utf8').split('\n')
    val = None
    for line in output :
        if not line.startswith('value = ') :
            continue
        return int(line[8:],16)
    return 0x0

def set_coef(reg, val) :
    execVerb(0x20, 0x500 | ((reg >> 8) & 0xFF), reg & 0xFF)
    execVerb(0x20, 0x400 | ((val >> 8) & 0xFF), val & 0xFF)

def get_coef(reg) :
    execVerb(0x20, 0x500 | ((reg >> 8) & 0xFF), reg & 0xFF)
    return execVerb(0x20, 0xc00, 0x0)

def update_coef(reg, orMask, notAndMask=0x0) :
    val = get_coef(reg)
    set_coef(reg, (val | orMask) & ~notAndMask)

def check_coef(reg, val) :
    ret = get_coef(reg)
    if ret != val :
        print('Value for reg 0x%X is not 0x%X but 0x%X' % (reg, val, ret))
        return False
    return True


def initAmpParams(reg23, reg25, reg22=None) :
    #Read vendor 8 times
    for i in range(8) :
        execVerb(0x0, 0xF00, 0x0)
    #nid 6: 0x00673e80
    execVerb(0x6, 0x73E, 0x80)
    update_coef(0x26, 0x4000)
    if reg22 :
        set_coef(0x22, reg22)
    set_coef(0x23, reg23)
    set_coef(0x25, reg25)

    set_coef(0x26, 0xb010)
    #Read vendor 8 times
    for i in range(8) :
        execVerb(0x0, 0xF00, 0x0)
    #nid 6: 0x00673e00
    execVerb(0x6, 0x73E, 0x00)
    update_coef(0x26, 0x0, 0x10)
    check_coef(0x26, 0xb000)

def setRegs(values, state) :
    for (reg23, reg25) in values :
        while get_coef(0x26) & 0x4000 :#XXX : retourne initialement 0xB000 puis 0xB003 puis parfois 0xF013 (alors on attend et on relit ?)
            pass
        set_coef(0x23, reg23)
        set_coef(0x24, 0x0)
        set_coef(0x25, reg25)
        set_coef(0x26, 0xb013)
