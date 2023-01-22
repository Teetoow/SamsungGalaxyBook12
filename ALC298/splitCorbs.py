#!/usr/bin/python3
#
#    splitCorbs.py             (C) 2022-2023, Aurélien Croc (AP²C)
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
import os


nidRe = re.compile('.* nid=0x([0-9a-f]+), .*')

if len(sys.argv) < 2 :
    print('Usage: %s <corb file>' % sys.argv[0])
    print('   - to read file from stdin')
    sys.exit(0)
if sys.argv[1] == '-' :
    f = sys.stdin
    prefixFile = 'output'
else :
    f = open(sys.argv[1], 'r')
    prefixFile = os.path.basename(sys.argv[1]).split('.')[0]

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

files={}
i=0
unsolTags = {}
tagByNid = {}
for l in cmd :
    if l == '#unsolicited' :
        v = int(ret[i], base=16)
        tag = (v >> 26) & 0x3F
        if tag in unsolTags :
            for n in unsolTags[tag] :
                files[n].write('# [%i] Unsolicited response: tag=%x, subtag=%x,'
                    ' data=%x\n' % (i, tag, (v>>21) & 0x1F, v & 0xFFFFF))
        else :
            files[0].write('# [%i] Unsolicited response: tag=%x, subtag=%x, '
                'data=%x\n', (i, tag, (v>>21) & 0x1F, v & 0xFFFFF))
        i += 1
        continue
    res = nidRe.match(l)
    if not res :
        print('error %s' % l)
        continue
    nid = res.group(1)
    if nid not in files :
        f = prefixFile + '-' + nid + '.txt'
        files[nid] = open(f, 'w')
    files[nid].write('[%s] %s => %s\n' % (i, l, ret[i]))
    if 'set_unsol_enable' in l :
        v = int(l.split(':')[0], base=16)
        if v & 0x80 :
            tag = v & 0x3F
            tagByNid[nid] = tag
            if tag not in unsolTags :
                unsolTags[tag] = [nid,]
            elif nid not in unsolTags[tag] :
                unsolTags[tag].append(nid)
        elif tag in tagByNid :
            unsolTags[tagByNid[tag]].remove(nid)
            del tagByNid[tag]
        
    i += 1
