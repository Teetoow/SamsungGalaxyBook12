#!/usr/bin/python3
#
#    dpAux.py                  (C) 2022-2023, Aurélien Croc (AP²C)
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

class DPAux :
    def __init__(self) :
        self.f = None

    def open(self, path='/dev/drm_dp_aux0') :
        self.f = open(path, 'r+b', buffering=0)

    def reopen(self) :
        self.f.close()
        self.open()

    def read(self, addr) :
        self.f.seek(addr, 0)
        return int.from_bytes(self.f.read(1), byteorder="little")

    def write(self, addr, val) :
        self.f.seek(addr, 0)
        return self.f.write((val).to_bytes(1, byteorder='little', signed=False))

    def writeArray(self, array) :
        for (addr, val) in array :
            # Send multiple bytes
            if isinstance(val, list) or isinstance(val, tuple) :
                self.f.seek(addr, 0)
                for i in val :
                    self.f.write((i).to_bytes(1, byteorder='little', signed=False))
            # Send single byte
            else :
                self.write(addr, val)
