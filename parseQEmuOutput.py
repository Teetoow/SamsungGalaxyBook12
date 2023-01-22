#!/usr/bin/env python3
#
#    parseQEmuOutput.py        (C) 2022-2023, Aurélien Croc (AP²C)
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
import subprocess
import sys
import re

def getCorb(c) :
    print(extractVerb(int(c, base=16)))
    #output = subprocess.run(['hda-decode-verb',c],capture_output=True).stdout.decode('utf8').split('\n')
    #nid = '???'
    #verb = 'Unknown'
    #parameter = ''
    #for line in output :
        #if line.startswith('cid = ') :
            #nid = line.split(' ')[5]
        #if line.startswith('verbname = ') :
            #verb = line.split(' ',3)[2]
        #elif line.startswith('parameter = ') :
            #parameter = ', param: ' + line.split(' ',3)[2]
    #print('%s: nid=%s %s%s' % (c, nid, verb, parameter))

if len(sys.argv) == 1 :
    print("Usage: %s <CORB file>" % sys.argv[0])
    sys.exit(-1)

f = open(sys.argv[1])

for line in f :
    if line.startswith('   RET') :
        print(line.replace('\n',''))
        continue
    getCorb(line.replace('\n',''))
