#!/usr/bin/env python3
#
#    addTimeToCorbs.py         (C) 2022-2023, Aurélien Croc (AP²C)
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
import sys
import re

# 39676@1670001694.038647:vfio_region_write  (0000:00:1f.3:region0+0x48, 0x2, 2)

writeLine = re.compile('[0-9]+@([0-9\.]+):vfio_region_write  \(....:..:..\..:region0\+0x48, 0x([0-9a-f]+),.*')

if len(sys.argv) < 3 :
    print("Usage: %s <qemu output file> <CORB2 file>" % sys.argv[0])
    sys.exit(-1)

qemu = open(sys.argv[1])
corb = open(sys.argv[2])
baseTime = 0
last = 0
for line in qemu :
    res = writeLine.search(line)
    if not res :
        continue

    curTime = float(res.group(1))
    newIdx = int(res.group(2), base=16)
    if baseTime == 0 :
        baseTime = curTime
        last = newIdx
        continue
 
    while last != newIdx :
        corbLine = corb.readline()
        print('%s: %s' % (curTime - baseTime, corbLine), end='')
        last += 1
        if last == 0x100 :
            last = 0
