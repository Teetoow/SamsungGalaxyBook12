#!/usr/bin/python3
#
#    parseProcCoef.py          (C) 2022-2023, Aurélien Croc (AP²C)
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
import sys
import re

rawRe = re.compile('.*\[([0-9]+)\] 0x([0-9a-f]+): .*')
resRe = re.compile('.*\[([0-9]+)\] .*=>  0x([0-9a-f]+)$')

if len(sys.argv) < 2 :
    print('Usage: %s <corb file>' % sys.argv[0])
    print('   - to read file from stdin')
    sys.exit(0)

if sys.argv[1] == '-' :
    f = sys.stdin
else :
    f = open(sys.argv[1], 'r')
idx=0

wasGet=None
def checkWasGet(getTuple, elemNr=None, setIdx=None, setVal=None) :
    if getTuple == None :
        return False

    if setIdx == getTuple[1] :
        print('[%s] Update %x: %x -> %x (XOR 0x%04x)' % (getTuple[3], setIdx, \
            getTuple[2], setVal, setVal ^ getTuple[2]))
        return True
    #if elemNr == getTuple[0] + 1 :
        #if setIdx == getTuple[1] :
            #print('[%s] Update %x: %x -> %x (XOR 0x%04x)' % (getTuple[3], setIdx, \
                #getTuple[2], setVal, setVal ^ getTuple[2]))
            #return True
    print('[%s] Get %x: %x' % (getTuple[3], getTuple[1], getTuple[2]))
    return False
    
elemNr = 0
for line in f :
    if line[0] == '#' :
        continue
    if 'set_coef_index' in line :
        res = rawRe.match(line)
        if not res :
            print("Error while getting raw value")
            continue
        val = int(res.group(2), base=16)
        idx = val & 0xFFFF
    elif 'get_proc_coef' in line :
        res = resRe.match(line)
        if not res :
            print("Error while getting res value")
            continue
        checkWasGet(wasGet)
        wasGet = (elemNr, idx, int(res.group(2), base=16), res.group(1))
        #print('[%s] Get %x: %x' % (res.group(1), idx, int(res.group(2), base=16)))
        idx += 1
        elemNr += 1
    elif 'set_proc_coef' in line :
        res = rawRe.match(line)
        if not res :
            print("Error while getting raw value")
            continue
        val = int(res.group(2), base=16) & 0xFFFF
        if not checkWasGet(wasGet, elemNr, idx, val) :
        #if True :
            print('[%s] Set %x: %x' % (res.group(1), idx, val))
        wasGet = None
        idx += 1
        elemNr += 1
    else :
        if line != '\n' :
            checkWasGet(wasGet)
            print("Unknown: %s" % line, end='')
            wasGet = None
        else :
            print()
        elemNr += 1

checkWasGet(wasGet)

