#!/usr/bin/python3
#
#    lineCorb.py               (C) 2022-2023, Aurélien Croc (AP²C)
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


nidRe = re.compile('.* nid=0x([0-9a-f]+), .*')

if len(sys.argv) < 2 :
    print('Usage: %s <corb file> [1 for only NID 0x6 and 0x20]' % sys.argv[0])
    print('   - to read file from stdin')
    sys.exit(0)

onlyNID6_20 = False
if len(sys.argv) == 3 :
    onlyNID6_20 = True if sys.argv[2] == '1' else False

if sys.argv[1] == '-' :
    f = sys.stdin
else :
    f = open(sys.argv[1], 'r')


nCmds=0
cmd=[]
ret=[]
for line in f :
    line = line.replace('\n', '')
    if line.startswith('   RET: ') :
        if nCmds :
            nCmds -= 1
        else :
            cmd.append('#unsolicited')
        ret.append(line.split(':')[1])
    else: 
        cmd.append(line)
        nCmds += 1
if nCmds :
    print("# Missing %i responses..." % nCmds)

i=0
wasGood=False
for l in cmd :
    if l == '#unsolicited' :
        v = int(ret[i], base=16)
        print('# Unsolicited response: tag=%x, subtag=%x, data=%x' % ((v>>26) & 0x3F, (v>>21) & 0x1F, v & 0xFFFFF))
        wasGood = True
        i += 1
        continue
    res = nidRe.match(l)
    if not res :
        print('error %s' % l)
        continue
    nid = res.group(1)
    if onlyNID6_20 and nid != "00" and nid != '06' and nid != '20' :
       if wasGood :
           print()
           wasGood = False
       i += 1
       continue
    print('[%s] %s => %s' % (i, l, ret[i]))
    wasGood = True
    i += 1
