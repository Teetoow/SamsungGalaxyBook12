#!/usr/bin/env python3
#
#    setHeadphone.py           (C) 2022-2023, Aurélien Croc (AP²C)
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
from verbUI import *
import sys

if len(sys.argv) == 1 :
    print("Usage: %s <0|1>" % sys.argv[0])
    print("   0 = internal speaker")
    print("   1 = external headphone")
    sys.exit(0)
if sys.argv[1] == '0' :
    tableSet1 = ((0x7a, 0x400), (0x61, 0xa000), (0x62, 0x8400), (0x194, 0x240), (0x10, 0x0)) # Enceintes
else :
    tableSet1 = ((0x7a, 0x6), (0x61, 0x8100), (0x62, 0x400), (0x194, 0x0), (0x10, 0x4040),) # Ecouteur

set_coef(0x22, 0x1b)
setRegs(tableSet1, False)
