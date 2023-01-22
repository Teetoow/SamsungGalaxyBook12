#!/usr/bin/env python3
#
#    verbToPython.py           (C) 2022-2023, Aurélien Croc (AP²C)
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

import shutil
import sys
import os
import re

lineRe = re.compile('.*\[([0-9]*)\] .*$')
getRe = re.compile('.*\[[0-9]*\] Get ([0-9a-f]+): ([0-9a-f]+)$')
setRe = re.compile('.*\[[0-9]*\] Set ([0-9a-f]+): ([0-9a-f]+)$')
updateRe = re.compile('.*\[[0-9]*\] Update ([0-9a-f]+): ([0-9a-f]+) -> ([0-9a-f]+) .*$')
update26Xor4000 = re.compile('.*\[[0-9]*\] Update 26: .* \(XOR 0x4000\)$')

if len(sys.argv) < 2 :
    print("Usage: %s <file> [<write line each N>]" % sys.argv[0])
    print('   - to read file from stdin')
    sys.exit(0)
if sys.argv[1] == '-' :
    f = sys.stdin
else :
    f = open(sys.argv[1], 'r')
if len(sys.argv) >= 3 :
    writeLine = int(sys.argv[2])
else :
    writeLine = 0

def findUpdateOrAndNotMask(valA, valB) :
    if valA == valB :
        return (valA, 0)
    andAB = valA & valB
    andNotMask = valA & ~andAB
    orMask = valB & ~andAB
    return (orMask, andNotMask)

tableNr = 1
setList = []
def purgeSet() :
    global tableNr, setList

    if not setList :
        return

    if len(setList) < 4 :
        for (idx, val) in setList :
            print("set_coef(0x%s, 0x%s)" % (idx, val))
        setList = []
        return

    name = 'tableSet%i' % tableNr
    tableNr += 1
    print('%s = (' % name, end='')
    for (idx, val) in setList :
        print('(0x%s, 0x%s), ' % (idx, val), end='')
    print(')\nfor (val, idx) in %s :\n    set_coef(val, idx)' % name)
    setList = []

ampRegs = []
def purgeAmpRegs() :
    global ampRegs, tableNr

    if not ampRegs :
        return
    subNr = 1
    tableNames = []
    parentName = 'tableSet%i' % tableNr
    tableNr += 1
    for (reg22, subList) in ampRegs :
        if len(subList) == 1 :
            continue
        name = '%s_%i' % (parentName, subNr)
        subNr += 1
        tableNames.append(name)
        print('%s = (' % name, end='')
        for (reg23, reg25) in subList :
            print('(0x%s, 0x%s), ' % (reg23, reg25), end='')
        print(')')

    print('%s = (' % parentName, end='')
    for (reg22, subList) in ampRegs :
        if len(subList) == 1 :
            print('(0x%s, ((0x%s, 0x%s),)), ' % (reg22, subList[0][0], subList[0][1]), end='')
            continue
        name = tableNames.pop(0)
        print('(0x%s, %s), ' % (reg22, name), end='')
    print(')')
    print('for (reg22, subTable) in %s :' % parentName)
    print('    for (reg23, reg25) in subTable :')
    print('        initAmpParams(reg23, reg25, reg22)')
    print('        reg22 = None')
    ampRegs = []

regValues = []
withNID06 = False
def purgeRegValues() :
    global regValues, tableNr, withNID06

    if not regValues :
        return

    name = 'tableSet%i' % tableNr
    tableNr += 1

    print('%s = (' % name, end='')
    for (reg23, reg25) in regValues :
        print('(0x%s, 0x%s), ' % (reg23, reg25), end='')
    print(')')
    print('setRegs(%s, %s)' % (name, withNID06))
    regValues = []

def purgeCmds(nextCmd='') :
    if nextCmd != 'set' :
        purgeSet()
    purgeAmpRegs()
    purgeRegValues()

# Copy verbUI.py file if needed
if not os.path.exists('verbUI.py') :
    scriptDir = os.path.dirname(sys.argv[0])
    if scriptDir != '' :
        shutil.copyfile(scriptDir + '/verbUI.py', 'verbUI.py') 


lastLineGroup = -1
state = 0
subState = 0
print('#!/usr/bin/env python3')
print('from verbUI import *')
print()
for line in f :
    # Avoid empty lines
    line = line.replace('\n', '')
    if line == '' or line == 'Unknown: ' :
        continue

    # Write line if needed
    if writeLine > 0 :
        res = lineRe.match(line)
        if res :
            tmp = int(res.group(1))
            lineGroup = int(tmp / writeLine)
            if lineGroup > lastLineGroup :
                print('# Line %i' % tmp)
                lastLineGroup = lineGroup

    # Amp parameter settings
    if state == 1 :
        if subState == 0 and 'nid=0x00, get_parameters, param: vendor' in line :
            continue
        if subState == 0 and '0x00673e80: nid=0x06, ' in line :
            subState = 1
            continue
        if subState == 0 and '0x00673e00: nid=0x06, ' in line :
            subState = 3
            continue
        if subState == 0 and 'Get 26:' in line :
            continue
        if subState == 1 :
            res = update26Xor4000.match(line)
            if res :
                subState = 2
                continue
        if subState == 2 :
            reg = None
            res = setRe.match(line)
            if res :
                reg = res.group(1)
                val = res.group(2)
            else :
                res = updateRe.match(line)
                if res :
                    reg = res.group(1)
                    val = res.group(3)
            if reg :
                if reg == '22' :
                    ampRegs.append((val, []))
                    continue
                elif reg == '23' :
                    ampRegs23 = val
                    continue
                elif reg == '25' :
                    ampRegs25 = val
                    continue
                elif reg == '26' and val == 'b010' :
                    ampRegs[-1][1].append((ampRegs23, ampRegs25))
                    ampRegs23 = None
                    ampRegs25 = None
                    subState = 0
                    continue
        if subState == 3 and 'Update 26:' in line :
            subState = 0
            continue
        state = 0

    # Reg initialization
    elif state == 2 :
        if subState == 0 :
            if '0x00673e80: nid=0x06, ' in line :
                withNID06 = True
                continue
            if '0x00673e00: nid=0x06, ' in line :
                withNID06 = True
                continue
            res = getRe.match(line)
            if res and res.group(1) == '26' :
                if res.group(2) != 'b000' and res.group(2) != 'b003' :
                    print('# Reg 26 contains 0x%s' % res.group(2))
                else :
                    subState = 1
                    reg23 = None
                    reg25 = None
                continue
        if subState == 1 :
            res = setRe.match(line)
            if res :
                if res.group(1) == '23' :
                    reg23 = res.group(2)
                    continue
                elif res.group(1) == '24' :
                    if res.group(2) != '0' :
                        print("# Reg 24 not null")
                    continue
                elif res.group(1) == '25' :
                    reg25 = res.group(2)
                    continue
                elif res.group(1) == '26' :
                    if res.group(2) != 'b013' :
                        print("# Reg 26 not set to 0xB013")
                    else :
                        regValues.append((reg23, reg25))
                        subState = 0
                    continue
        state = 0

    # Basic state
    if state == 0 :
        # Check for a get command
        res = getRe.match(line)
        if res :
            purgeCmds()
            print('check_coef(0x%s, 0x%s)' % (res.group(1), res.group(2)))
            if res.group(1) == '26' and res.group(2) == 'b003' :
                state = 2
                subState = 1
                withNID06 = False
                continue
            continue
        # Check for a set command
        res = setRe.match(line)
        if res :
            # Check whether set regs is starting
            if res.group(1) == '22' and res.group(2) == '1b' :
                purgeCmds()
                state = 2
                subState = 0
                print('set_coef(0x22, 0x1b)')
                continue

            purgeCmds('set')
            setList.append((res.group(1), res.group(2)))
            continue
        # Check for an update command
        res = updateRe.match(line)
        if res :
            purgeCmds()
            (orMask, andNotMask) = findUpdateOrAndNotMask(
                int(res.group(2), base=16), int(res.group(3), base=16))
            if andNotMask :
                print('update_coef(0x%s, 0x%x, 0x%x)' % (res.group(1), orMask, andNotMask))
            else :
                print('update_coef(0x%s, 0x%x)' % (res.group(1), orMask))
            continue

    # Check for amp parameters setting
    if 'nid=0x00, get_parameters, param: vendor' in line :
        purgeCmds()
        state = 1
        subState = 0
        continue

    # Unknown line
    print('# Unknown: %s' % line)

purgeCmds()

