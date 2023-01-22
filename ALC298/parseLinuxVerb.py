#!/usr/bin/python3
#
#    parseLinuxVerb.py         (C) 2022-2023, Aurélien Croc (AP²C)
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
from extractVerb import extractVerb
import sys
import re

if len(sys.argv) < 2 :
    print("Usage: %s <hda verb file>" % sys.argv[0])
    print('   - to read file from stdin')
    sys.exit(0)

if sys.argv[1] == '-' :
    f = sys.stdin
else :
    f = open(sys.argv[1], 'r')

valRe = re.compile('.* val=0x([0-9a-f]*)$')

cmds=[]
rets=[]
i=0
for line in f :
    i += 1
    if line.startswith('#') :
        continue
    if 'hda_send_cmd' in line :
        res = valRe.match(line)
        if not res :
            print("Error line %i" % i)
            continue
        cmds.append(int(res.group(1), base=16))
    elif 'hda_get_response' in line :
        res = valRe.match(line)
        if not res :
            print("Error line %i" % i)
            continue
        rets.append(int(res.group(1), base=16))
    else :
        print("Unknown line")

i=0
for v in cmds :
    print(extractVerb(cmds[i]))
    print("   RET: 0x%08x" % rets[i])
    i += 1
