#!/usr/bin/python3
#
#    tables.py                 (C) 2022-2023, Aurélien Croc (AP²C)
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

# === brightnessDataF
registerValuesA = (
    (2, 0, 0), 
    (2, 0, 0x80), 
    (2, 1, 0), 
    (2, 1, 0x80), 
    (2, 2, 0), 
    (2, 2, 0x80), 
    (2, 3, 0), 
    (2, 3, 0x80), 
    (2, 4, 0), 
    (2, 4, 0x80), 
    (2, 5, 0), 
    (4, 0, 0), 
    (4, 0, 0x80), 
    (4, 1, 0), 
    (4, 1, 0x80), 
    (4, 2, 0), 
    (4, 2, 0x80), 
    (4, 3, 0), 
    (4, 3, 0x80), 
    (4, 4, 0), 
    (4, 4, 0x80), 
    (4, 5, 0), 
    (8, 0, 0), 
    (8, 0, 0x80), 
    (8, 1, 0), 
    (8, 1, 0x80), 
    (8, 2, 0), 
    (8, 2, 0x80), 
    (8, 3, 0), 
    (8, 3, 0x80), 
    (8, 4, 0), 
    (8, 4, 0x80), 
    (8, 5, 0), 
)

registerValuesB = (
    (2, 0xAA, 0x80), 
    (2, 0xAB, 0), 
    (2, 0xAB, 0x80), 
    (2, 0xAC, 0), 
    (2, 0xAC, 0x80), 
    (2, 0xAD, 0), 
    (2, 0xAD, 0x80), 
    (2, 0xAE, 0), 
    (2, 0xAE, 0x80), 
    (2, 0xAF, 0), 
    (2, 0xAF, 0x80), 
    (4, 0xAA, 0x80), 
    (4, 0xAB, 0), 
    (4, 0xAB, 0x80), 
    (4, 0xAC, 0), 
    (4, 0xAC, 0x80), 
    (4, 0xAD, 0), 
    (4, 0xAD, 0x80), 
    (4, 0xAE, 0), 
    (4, 0xAE, 0x80), 
    (4, 0xAF, 0), 
    (4, 0xAF, 0x80), 
    (8, 0xAA, 0x80), 
    (8, 0xAB, 0), 
    (8, 0xAB, 0x80), 
    (8, 0xAC, 0), 
    (8, 0xAC, 0x80), 
    (8, 0xAD, 0), 
    (8, 0xAD, 0x80), 
    (8, 0xAE, 0), 
    (8, 0xAE, 0x80), 
    (8, 0xAF, 0), 
    (8, 0xAF, 0x80), 
)

scalarVectorA = (0, 0xC, 0x18, 0x24, 0x30, 0x3C, 0x48, 0x54, 0x60, 0x6C, 0x8A,
    0x94, 0x9E, 0xA8, 0xB2, 0xBA)

adjustmentFactorA = [0] * 31
adjustmentFactorB = ( \
    0x40,
    0x140,
    0x40,
    0x140,
    0x40,
    0x140,
    0x40,
    0x140,
    0x40,
    0x140,
    0x40,
    0x140,
    0x40,
    0x140,
    0x40,
    0x140,
    0x81,
    0x280
)



# Data
ptrInto384Table = (
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 
    0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 
    0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 
    0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 
    0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x2F, 0x30, 
    0x30, 0x30, 0x31, 0x31, 0x31, 0x32, 0x32, 0x33, 0x33, 0x33, 
    0x34, 0x34, 0x34, 0x35, 0x35, 0x35, 0x36, 0x36, 0x36, 0x37,
    0x37, 0x37, 0x38, 0x38, 0x38, 0x39, 0x39, 0x39, 0x3A, 0x3A,
    0x3A, 0x3B, 0x3B, 0x3B, 0x3C, 0x3C, 0x3C, 0x3D, 0x3D, 0x3D, 
    0x3E, 0x3E, 0x3E, 0x3F, 0x3F, 0x3F, 0x40, 0x40, 0x40, 0x40,
    0x40, 0x40
)

structA = (
    0x04, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0B, 0x0C, 0x0D,
    0x0D, 0x0E, 0x0F, 0x10, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 
    0x16, 0x16, 0x17, 0x19, 0x1A, 0x1B, 0x1C, 0x1E, 0x1F, 0x20,
    0x21, 0x24, 0x26, 0x28, 0x2A, 0x2D, 0x2F, 0x32, 0x35, 0x38,
    0x3B, 0x40, 0x43, 0x48, 0x4C, 0x50, 0x55, 0x59, 0x5B, 0x5D,
    0x5F, 0x60, 0x62, 0x64, 0x66, 0x69, 0x6B, 0x6F, 0x71, 0x73,
    0x76, 0x78, 0x7A, 0x7C, 0x7F, 0x81, 0x84, 0x87, 0x8A, 0x8D,
    0x90, 0x92, 0x95, 0x99, 0x9C, 0x9E, 0xA3, 0xA6, 0xAA, 0xAD,
    0xB1, 0xB5, 0xB9, 0xBC, 0xC1, 0xC4, 0xC8, 0xCD, 0xD1, 0xD5,
    0xDB, 0xDE, 0xE1, 0xE7, 0xEA, 0xEE, 0xF2, 0xF5, 0xF8, 0xFC,
    0xF9, 0xF9
)
structB = (
    (1, 1, 1, 0, 0, 0, 0, 0, 0),
    (1, 1, 1, 0, 0, 0, 1, 1, 0),
    (1, 1, 1, 1, 1, 1, 0, 0, 0),
    (2, 2, 1, 0, 0, 1, 1, 1, 0),
    (2, 2, 2, 1, 1, 0, 0, 0, 1),
    (3, 3, 2, 0, 0, 1, 1, 1, 0),
    (3, 3, 2, 1, 1, 1, 0, 0, 0),
    (3, 3, 3, 1, 1, 0, 1, 1, 1),
    (4, 4, 3, 1, 0, 1, 0, 1, 0),
    (4, 4, 3, 1, 1, 1, 1, 1, 1),
    (4, 4, 3, 2, 1, 2, 0, 1, 0),
    (5, 5, 4, 1, 1, 1, 1, 1, 0),
    (5, 5, 4, 2, 1, 1, 0, 1, 1),
    (6, 5, 4, 1, 2, 2, 1, 1, 0),
    (6, 6, 5, 2, 1, 1, 0, 1, 1),
    (6, 6, 5, 2, 2, 1, 1, 1, 1),
    (7, 7, 5, 2, 1, 2, 1, 2, 1),
    (7, 7, 6, 2, 2, 2, 1, 2, 0),
    (8, 8, 6, 2, 1, 2, 1, 2, 1),
    (8, 8, 6, 2, 2, 2, 1, 2, 1),
    (9, 9, 7, 2, 2, 2, 1, 2, 1),
    (9, 9, 7, 3, 2, 2, 1, 2, 2),
    (0x0A, 0x0A, 8, 3, 2, 2, 1, 2, 1),
    (0x0B, 0x0A, 8, 3, 3, 3, 1, 2, 1),
    (0x0B, 0x0B, 9, 3, 2, 2, 1, 3, 2),
    (0x0C, 0x0B, 9, 3, 3, 3, 1, 3, 2),
    (0x0D, 0x0C, 0x0A, 3, 3, 3, 1, 3, 1),
    (0x0E, 0x0D, 0x0B, 3, 4, 3, 2, 3, 2),
    (0x0F, 0x0E, 0x0B, 3, 3, 4, 2, 4, 1),
    (0x0F, 0x0F, 0x0C, 4, 3, 3, 2, 4, 2),
    (0x10, 0x10, 0x0D, 5, 4, 4, 1, 3, 2),
    (0x11, 0x11, 0x0E, 5, 4, 4, 2, 4, 2),
    (0x13, 0x12, 0x0E, 4, 4, 5, 2, 5, 2),
    (0x14, 0x13, 0x0F, 5, 5, 5, 2, 4, 2),
    (0x15, 0x14, 0x10, 5, 5, 5, 2, 5, 3),
    (0x16, 0x16, 0x11, 6, 5, 6, 2, 5, 2),
    (0x18, 0x17, 0x12, 6, 6, 6, 2, 5, 3),
    (0x19, 0x18, 0x14, 7, 6, 6, 2, 6, 3),
    (0x1B, 0x1A, 0x15, 7, 6, 6, 2, 6, 3),
    (0x1D, 0x1C, 0x16, 7, 6, 7, 3, 7, 4),
    (0x1F, 0x1D, 0x18, 7, 8, 7, 3, 7, 4),
    (0x20, 0x1F, 0x19, 9, 8, 8, 3, 7, 4),
    (0x23, 0x21, 0x1B, 9, 9, 8, 3, 7, 4),
    (0x24, 0x23, 0x1C, 0x0A, 9, 9, 4, 8, 4),
    (0x27, 0x26, 0x1E, 0x0A, 9, 0x0A, 4, 9, 4),
    (0x29, 0x28, 0x20, 0x0B, 0x0A, 0x0A, 4, 9, 5),
    (0x2C, 0x2B, 0x22, 0x0C, 0x0A, 0x0B, 4, 0x0A, 5),
    (0x2E, 0x2C, 0x23, 0x0C, 0x0B, 0x0B, 4, 0x0A, 6),
    (0x2F, 0x2D, 0x24, 0x0C, 0x0B, 0x0C, 5, 0x0B, 5),
    (0x30, 0x2E, 0x25, 0x0C, 0x0C, 0x0C, 5, 0x0A, 5),
    (0x31, 0x2F, 0x26, 0x0D, 0x0C, 0x0C, 4, 0x0B, 5),
    (0x32, 0x30, 0x27, 0x0D, 0x0C, 0x0C, 5, 0x0B, 6),
    (0x33, 0x31, 0x28, 0x0D, 0x0C, 0x0C, 5, 0x0C, 6),
    (0x34, 0x32, 0x28, 0x0E, 0x0D, 0x0D, 5, 0x0B, 6),
    (0x35, 0x33, 0x29, 0x0E, 0x0D, 0x0D, 5, 0x0C, 6),
    (0x37, 0x35, 0x2B, 0x0E, 0x0D, 0x0D, 6, 0x0C, 6),
    (0x39, 0x36, 0x2C, 0x0E, 0x0E, 0x0D, 6, 0x0D, 7),
    (0x3A, 0x38, 0x2D, 0x0F, 0x0D, 0x0E, 6, 0x0D, 7),
    (0x3B, 0x39, 0x2E, 0x0F, 0x0E, 0x0E, 6, 0x0D, 7),
    (0x3C, 0x3A, 0x2F, 0x10, 0x0E, 0x0E, 6, 0x0E, 7),
    (0x3E, 0x3B, 0x30, 0x10, 0x0F, 0x0E, 6, 0x0E, 8),
    (0x3F, 0x3C, 0x31, 0x10, 0x0F, 0x0F, 6, 0x0E, 7),
    (0x40, 0x3E, 0x32, 0x11, 0x0F, 0x0F, 6, 0x0E, 8),
    (0x41, 0x3F, 0x33, 0x11, 0x10, 0x0F, 7, 0x0E, 8),
    (0x43, 0x40, 0x34, 0x11, 0x10, 0x10, 7, 0x0F, 8),
    (0x44, 0x42, 0x35, 0x12, 0x10, 0x10, 7, 0x0F, 8),
    (0x46, 0x43, 0x36, 0x12, 0x11, 0x11, 7, 0x0F, 8),
    (0x47, 0x44, 0x37, 0x13, 0x11, 0x11, 7, 0x10, 9),
    (0x49, 0x46, 0x38, 0x13, 0x11, 0x12, 7, 0x10, 8),
    (0x4A, 0x47, 0x39, 0x13, 0x12, 0x12, 8, 0x11, 9),
    (0x4C, 0x49, 0x3B, 0x13, 0x12, 0x12, 8, 0x11, 9),
    (0x4D, 0x4A, 0x3C, 0x14, 0x13, 0x12, 8, 0x11, 9),
    (0x4F, 0x4C, 0x3D, 0x14, 0x13, 0x13, 8, 0x11, 9),
    (0x50, 0x4D, 0x3E, 0x15, 0x13, 0x13, 8, 0x12, 0x0A),
    (0x52, 0x4F, 0x40, 0x15, 0x13, 0x13, 8, 0x13, 0x0A),
    (0x54, 0x51, 0x41, 0x15, 0x13, 0x14, 9, 0x13, 0x0A),
    (0x55, 0x52, 0x42, 0x17, 0x15, 0x15, 8, 0x13, 0x0A),
    (0x57, 0x54, 0x44, 0x17, 0x15, 0x14, 8, 0x13, 0x0B),
    (0x59, 0x56, 0x45, 0x17, 0x15, 0x15, 9, 0x14, 0x0B),
    (0x5B, 0x57, 0x46, 0x18, 0x16, 0x16, 8, 0x14, 0x0B),
    (0x5D, 0x59, 0x48, 0x18, 0x16, 0x16, 9, 0x15, 0x0B),
    (0x5F, 0x5B, 0x49, 0x18, 0x17, 0x17, 0x0A, 0x15, 0x0B),
    (0x61, 0x5D, 0x4B, 0x19, 0x17, 0x17, 9, 0x16, 0x0C),
    (0x63, 0x5F, 0x4D, 0x19, 0x18, 0x17, 0x0A, 0x16, 0x0C),
    (0x65, 0x61, 0x4E, 0x1A, 0x18, 0x18, 0x0A, 0x17, 0x0C),
    (0x67, 0x63, 0x50, 0x1B, 0x19, 0x18, 0x0A, 0x17, 0x0D),
    (0x69, 0x65, 0x51, 0x1B, 0x19, 0x1A, 0x0B, 0x18, 0x0C),
    (0x6B, 0x67, 0x53, 0x1C, 0x1A, 0x1A, 0x0B, 0x18, 0x0D),
    (0x6D, 0x69, 0x55, 0x1D, 0x1A, 0x1A, 0x0B, 0x19, 0x0D),
    (0x70, 0x6C, 0x57, 0x1D, 0x1A, 0x1A, 0x0B, 0x19, 0x0E),
    (0x72, 0x6D, 0x58, 0x1D, 0x1C, 0x1B, 0x0B, 0x19, 0x0E),
    (0x74, 0x6F, 0x5A, 0x1E, 0x1C, 0x1B, 0x0B, 0x1A, 0x0E),
    (0x76, 0x71, 0x5B, 0x1E, 0x1C, 0x1C, 0x0C, 0x1B, 0x0E),
    (0x78, 0x73, 0x5D, 0x1F, 0x1D, 0x1D, 0x0C, 0x1B, 0x0E),
    (0x7A, 0x75, 0x5F, 0x20, 0x1D, 0x1D, 0x0B, 0x1C, 0x0E),
    (0x7C, 0x77, 0x60, 0x20, 0x1E, 0x1E, 0x0C, 0x1C, 0x0F),
    (0x7E, 0x79, 0x62, 0x21, 0x1E, 0x1E, 0x0C, 0x1D, 0x0F),
    (0x80, 0x7B, 0x63, 0x21, 0x1F, 0x1F, 0x0D, 0x1C, 0x0F),
    (0x82, 0x7D, 0x65, 0x22, 0x1F, 0x1F, 0x0D, 0x1D, 0x0F),
    (0x84, 0x7F, 0x66, 0x22, 0x20, 0x20, 0x0D, 0x1D, 0x10),
    (0x86, 0x81, 0x68, 0x23, 0x20, 0x20, 0x0D, 0x1E, 0x10),
    (0, 0, 0, 0, 0, 0, 0, 0, 0)
)

structC = (
    (0x0B, 0x60),
    (0x0B, 0x48),
    (0x0B, 0x30),
    (0x0B, 0x18),
    (0x0B, 0),
    (0x0A, 0x0E8),
    (0x0A, 0x0D0),
    (0x0A, 0x0B8),
    (0x0A, 0x0A0),
    (0x0A, 0x88),
    (0x0A, 0x70),
    (0x0A, 0x58),
    (0x0A, 0x40),
    (0x0A, 0x28),
    (0x0A, 8),
    (9, 0x0F0),
    (9, 0x0C0),
    (9, 0x0A0),
    (9, 0x88),
    (9, 0x68),
    (9, 0x38),
    (9, 0x20),
    (8, 0x0E8),
    (8, 0x0B0),
    (8, 0x0A8),
    (8, 0x70),
    (8, 0x30),
    (7, 0x0D0),
    (7, 0x0B0),
    (7, 0x68),
    (7, 0x18),
    (6, 0x0B0),
    (6, 0x58),
    (5, 0x0F8),
    (5, 0x0A0),
    (5, 0x30),
    (4, 0x98),
    (4, 0x30),
    (4, 0x30),
    (4, 0x30),
    (4, 0x30),
    (4, 0x30),
    (4, 0x30),
    (4, 0x30),
    (4, 0x30),
    (4, 0x30),
    (4, 0x30),
    (4, 0x65),
    (4, 0x30),
    (4, 0x69),
    (4, 0x30),
    (4, 0x80),
    (4, 0x58),
    (4, 0x30),
    (4, 0x7B),
    (4, 0x55),
    (4, 0x30),
    (4, 0x7E),
    (4, 0x57),
    (4, 0x30),
    (4, 0x79),
    (4, 0x55),
    (4, 0x30),
    (4, 8),
    (3, 0x0E0),
    (3, 0x0B8),
    (3, 0x85),
    (3, 0x53),
    (3, 0x20),
    (2, 0x0F0),
    (2, 0x0C0),
    (2, 0x90),
    (2, 0x55),
    (2, 0x1B),
    (1, 0x0E0),
    (1, 0x0A8),
    (1, 0x70),
    (1, 0x38),
    (0, 0x0F5),
    (0, 0x0B3),
    (0, 0x70),
    (0, 0x0E3),
    (0, 0x0A9),
    (0, 0x70),
    (0, 0x0E3),
    (0, 0x0A9),
    (0, 0x70),
    (0, 0x0E2),
    (0, 0x0A9),
    (0, 0x70),
    (0, 0x0D0),
    (0, 0x0A0),
    (0, 0x70),
    (0, 0x0D1),
    (0, 0x0A1),
    (0, 0x70),
    (1, 0x1B),
    (0, 0x0F1),
    (0, 0x0C6),
    (0, 0x9B),
    (0, 0x70),
    (0, 0x70),
)

structC2 = (
    0x8C, 0x8C, 0x8C, 0x8C, 0x8C, 0x8C, 0x8C, 0x8C, 0x8C, 0x8C, 0x8C,
    0x8D, 0x8D, 0x8D, 0x8D, 0x8D, 0x8E, 0x8E, 0x8E, 0x8F, 0x8F, 0x8F,
    0x90, 0x90, 0x90, 0x91, 0x91, 0x92, 0x92, 0x93, 0x94, 0x94, 0x95,
    0x96, 0x96, 0x97, 0x98, 0x98, 0x98, 0x98, 0x98, 0x98, 0x98, 0x98,
    0x97, 0x97, 0x96, 0x96, 0x95, 0x94, 0x94, 0x93, 0x93, 0x93, 0x92,
    0x92, 0x92, 0x91, 0x91, 0x90, 0x8F, 0x8E, 0x8D, 0x8C, 0x8A, 0x8A 
)

structC_cc5False = (
    (0x0B, 0x70),
    (0x0B, 0x58),
    (0x0B, 0x40),
    (0x0B, 0x28),
    (0x0B, 0x18),
    (0x0B, 0),
    (0x0A, 0x0E8),
    (0x0A, 0x0D0),
    (0x0A, 0x0C0),
    (0x0A, 0x0A8),
    (0x0A, 0x90),
    (0x0A, 0x78),
    (0x0A, 0x60),
    (0x0A, 0x48),
    (0x0A, 0x38),
    (0x0A, 0x20),
    (9, 0x0F0),
    (9, 0x0D8),
    (9, 0x0C0),
    (9, 0x0A8),
    (9, 0x80),
    (9, 0x68),
    (9, 0x38),
    (9, 8),
    (8, 0x0F0),
    (8, 0x0C8),
    (8, 0x98),
    (8, 0x50),
    (8, 0x20),
    (7, 0x0F0),
    (7, 0x0A8),
    (7, 0x60),
    (7, 0x10),
    (6, 0x0C8),
    (6, 0x80),
    (6, 0x18),
    (5, 0x0B8),
    (5, 0x50),
    (4, 0x0E8),
    (4, 0x60),
    (4, 0x60),
    (4, 0x60),
    (4, 0x60),
    (4, 0x60),
    (4, 0x60),
    (4, 0x60),
    (4, 0x60),
    (4, 0x93),
    (4, 0x60),
    (4, 0x0AA),
    (4, 0x85),
    (4, 0x60),
    (4, 0x0AE),
    (4, 0x87),
    (4, 0x60),
    (4, 0x97),
    (4, 0x60),
    (4, 0x0AC),
    (4, 0x86),
    (4, 0x60),
    (4, 0x0A8),
    (4, 0x84),
    (4, 0x60),
    (4, 0x33),
    (4, 5),
    (3, 0x0D8),
    (3, 0x0A5),
    (3, 0x73),
    (3, 0x40),
    (3, 0x0B),
    (2, 0x0D5),
    (2, 0x0A0),
    (2, 0x68),
    (2, 0x30),
    (1, 0x0F8),
    (1, 0x0B8),
    (1, 0x78),
    (1, 0x38),
    (0, 0x0F5),
    (0, 0x0B3),
    (0, 0x70),
    (0, 0x0E3),
    (0, 0x0A9),
    (0, 0x70),
    (0, 0x0E3),
    (0, 0x0A9),
    (0, 0x70),
    (0, 0x0E2),
    (0, 0x0A9),
    (0, 0x70),
    (0, 0x0D0),
    (0, 0x0A0),
    (0, 0x70),
    (0, 0x0D1),
    (0, 0x0A1),
    (0, 0x70),
    (1, 0x1B),
    (0, 0x0F1),
    (0, 0x0C6),
    (0, 0x9B),
    (0, 0x70),
    (0, 0x70),
)

colorProfile0 = [0x98, 0x24, 0x0B3, 1, 0x0E, 1, 0, 0x77, 0x17, 3, 0x96, 0,
    0x0FF, 0, 0, 7, 0x0FF, 7, 0x0FF, 0x14, 0, 0x0A, 0, 0x32, 1, 0x0F4, 0x0B, 0x8A,
    0x20, 0x2D, 1, 0, 0, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90,
    0x0A0, 0x0B0, 0x0C0, 0x0E0, 0x0F0, 1, 0, 0, 0, 0, 0, 0, 0x40, 0x67, 0x0A9, 0x17,
    0x29, 0x19, 0x27, 0, 0x59, 0x0B, 0, 0x31, 0x0F4, 0, 0x51, 0x0EC, 0, 0x34, 0x83,
    0x0FF, 0x50, 0x60, 0x0FF, 0x0FF, 0, 0x0FF, 0, 0x0FF, 0x0FF, 0x0FF, 0x0FF, 0x97,
    0x0D3, 0x0F5, 0x27, 0x0EC, 0x26, 0x0E0, 0x8A, 0x40, 0x0EA, 0x0E0, 0x4C, 0x0F3,
    0x36, 0x0F0, 0x31, 0x5E, 0x0D8, 0x0FF, 0, 0x0FA, 0, 0x0F0, 0, 1, 0, 0x3E, 0, 0,
    8, 0x70, 5, 0x0A0]

colorProfile1 = [0x98, 0x24, 0x0B3, 1, 0x0E, 1, 0, 0x77, 0x17, 3, 0x96, 3,
    0x0FF, 0, 0, 7, 0x0FF, 7, 0x0FF, 0x14, 0, 0x0A, 0, 0x32, 1, 0x0F4, 0x0B, 0x8A,
    0x28, 0x3C, 1, 0x20, 0, 0x0A, 0x17, 0x26, 0x36, 0x49, 0x5C, 0x6F, 0x82, 0x95,
    0x0A8, 0x0BB, 0x0CB, 0x0DB, 0x0EB, 0x0F8, 1, 0, 0, 0, 0, 0, 0x30, 0x67, 0x0A9,
    0x37, 0x29, 0x19, 0x47, 0, 0x25, 0x3D, 0, 0x31, 0x0F4, 0, 0x51, 0x0EC, 0, 0x1C,
    0x0D8, 0x0FF, 0x42, 0x62, 0x0FF, 0x0FF, 0, 0x0FF, 0, 0x0FF, 0x0FF, 0x0F4, 0x0FF,
    0, 0x0FF, 0x0FF, 0, 0x0FF, 0, 0x0FF, 0, 0, 0x0FF, 0x0FF, 0, 0x0FF, 0, 0x0FF, 0,
    0, 0x0FF, 0x0FF, 0, 0x0FF, 0, 0x0FF, 0, 1, 0, 0x3E, 0, 0, 8, 0x70, 5, 0x0A0]

colorProfile2 = [0x98, 0x24, 0x0B3, 1, 0x0E, 1, 0, 0x77, 0x17, 3, 0x96, 0,
    0x0FF, 0, 0, 7, 0x0FF, 7, 0x0FF, 0x14, 0, 0x0A, 0, 0x32, 1, 0x0F4, 0x0B, 0x8A,
    0x20, 0x2D, 1, 0, 0, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90,
    0x0A0, 0x0B0, 0x0C0, 0x0E0, 0x0F0, 1, 0, 0, 0, 0, 0, 0, 0x40, 0x67, 0x0A9, 0x17,
    0x29, 0x19, 0x27, 0, 0x59, 0x0B, 0, 0x31, 0x0F4, 0, 0x51, 0x0EC, 0, 0x34, 0x83,
    0x0FF, 0x50, 0x60, 0x0FF, 0x0FF, 0, 0x0FF, 0, 0x0FF, 0x0FF, 0x0FF, 0x0FF, 0,
    0x0F1, 0x0F1, 0x29, 0x0E9, 0x2F, 0x0FD, 0, 0x4A, 0x0FF, 0x0E6, 0x2B, 0x0F2,
    0x34, 0x0EF, 0x33, 0x4B, 0x0E0, 0x0FF, 0, 0x0FA, 0, 0x0F0, 0, 1, 0, 0x3E, 0, 0,
    8, 0x70, 5, 0x0A0]

colorProfile3 = [0x98, 0x24, 0x0B3, 1, 0x0E, 1, 0, 0x77, 0x17, 3, 0x96, 2,
    0x0FF, 0, 0x60, 1, 0, 1, 0, 0x14, 0, 1, 0, 1, 0, 0x60, 0x3F, 0x0FF, 0x28, 0x3C,
    1, 0, 0, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90, 0x0A0, 0x0B0,
    0x0C0, 0x0E0, 0x0F0, 1, 0, 0, 0, 0, 0, 0, 0x30, 0x6A, 0x9A, 0x25, 0x1A, 0x16,
    0x2A, 0, 0x37, 0x5A, 0, 0x4E, 0x0C5, 0, 0x5D, 0x17, 0, 0x30, 0x0C3, 0x0FF, 0x3B,
    0x50, 0x0FF, 0x0F0, 0, 0x0D8, 0, 0x0D9, 0x0FF, 0x0FF, 0x0FF, 0, 0x0E0, 0x0FF, 0,
    0x0F6, 0, 0x0D8, 0x3B, 0, 0x0FF, 0x0D9, 0, 0x0FF, 0x14, 0x0F9, 0, 0, 0x0FF,
    0x0FF, 0, 0x0FF, 0, 0x0FF, 0, 1, 0, 0x3E, 0, 0, 8, 0x70, 5, 0x0A0]

colorProfile4 = [0x98, 0x24, 0x0B3, 1, 0x0E, 1, 0, 0x77, 0x17, 3, 0x96, 0,
    0x0FF, 0, 0x60, 1, 0, 1, 0, 0x14, 0, 1, 0, 1, 0, 0x60, 0x3F, 0x0FF, 0x28, 0x3C,
    1, 0, 0, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90, 0x0A0, 0x0B0,
    0x0C0, 0x0E0, 0x0F0, 1, 0, 0, 0, 0, 0, 0, 0, 0x6A, 0x9A, 0x25, 0x1A, 0x16, 0x2A,
    0, 0x37, 0x5A, 0, 0x4E, 0x0C5, 0, 0x5D, 0x17, 0, 0x30, 0x0C3, 0x0FF, 0x28, 0x40,
    0x0FF, 0x0F0, 0, 0x0D8, 0, 0x0D9, 0x0FF, 0x0FF, 0x0FF, 0, 0x0FF, 0x0FF, 0,
    0x0FF, 0, 0x0FF, 0, 0, 0x0FF, 0x0FF, 0, 0x0FF, 0, 0x0FF, 0, 0, 0x0FF, 0x0FF, 0,
    0x0F9, 0, 0x0E9, 0, 1, 0, 0x3C, 0, 0, 8, 0x70, 5, 0x0A0]

colorProfile5 = (0x86, 0x0C, 0x0F0, 1, 0x0E, 1, 0, 0x77, 0x17, 0, 0x96, 0,
    0x0FF, 0, 0x30, 0, 0x0A0, 0, 0x0A0, 0x14, 0, 0x0A, 0, 0x32, 1, 0x0F4, 0x0B,
    0x8A, 0x20, 0x2D, 1, 0x40, 0, 0x21, 0x38, 0x4C, 0x5D, 0x6E, 0x7D, 0x8C, 0x9A,
    0x0A8, 0x0B5, 0x0C2, 0x0CF, 0x0DC, 0x0E8, 0x0F5, 1, 0, 0, 0, 0, 0, 0, 0x67,
    0x0A9, 0x17, 0x29, 0x19, 0x27, 0, 0x59, 0x0B, 0, 0x31, 0x0F4, 0, 0x51, 0x0EC, 0,
    0x34, 0x83, 0x0FF, 0x30, 0x30, 0x0FF, 0x0FF, 0, 0x0FF, 0, 0x0FF, 0x0FF, 0x0FF,
    0x0FF, 0, 0x0E0, 0x0FF, 0, 0x0F6, 0, 0x0D8, 0x3B, 0, 0x0FF, 0x0D9, 0, 0x0FF,
    0x14, 0x0F9, 0, 0, 0x0FF, 0x0FF, 0, 0x0FF, 0, 0x0FF, 0, 1, 0, 0x3F, 0, 0, 8,
    0x70, 5, 0x0A0)

colorProfile6 = (0x98, 0x24, 0x0B3, 1, 0x0E, 1, 0, 0x77, 0x17, 3, 0x96, 2,
    0x0FF, 0, 0x60, 1, 0, 1, 0, 0x14, 0, 1, 0, 1, 0, 0x60, 0x3F, 0x0FF, 0x28, 0x3C,
    1, 0, 0, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90, 0x0A0, 0x0B0,
    0x0C0, 0x0E0, 0x0F0, 1, 0, 0, 0, 0, 0, 0, 0x30, 0x6A, 0x9A, 0x25, 0x1A, 0x16,
    0x2A, 0, 0x37, 0x5A, 0, 0x4E, 0x0C5, 0, 0x5D, 0x17, 0, 0x30, 0x0C3, 0x0FF, 0x28,
    0x40, 0x0FF, 0x0F0, 0, 0x0D8, 0, 0x0D9, 0x0FF, 0x0FF, 0x0FF, 0, 0x0E0, 0x0FF, 0,
    0x0F6, 0, 0x0D8, 0x3B, 0, 0x0FF, 0x0D9, 0, 0x0FF, 0x14, 0x0F9, 0, 0, 0x0FF,
    0x0FF, 0, 0x0FA, 0, 0x0F0, 0, 1, 0, 0x3E, 0, 0, 8, 0x70, 5, 0x0A0)

colorProfileAdjTableA = (0x0FF, 0x0FF, 0x0FF, 0x0FF, 0x0FB, 0x0FB, 0x0FF, 0x0FC,
    0x0FF, 0x0FB, 0x0F9, 0x0FF, 0x0FF, 0x0FE, 0x0FC, 0x0FF, 0x0FF, 0x0FF, 0x0FB,
    0x0FC, 0x0FF, 0x0FD, 0x0FF, 0x0FB, 0x0FB, 0x0FF, 0x0FC, 0x0FB, 0x0FF, 0x0FF)

colorProfileAdjTableB = (0x0FF, 0x0FF, 0x0FF, 0x0FF, 0x0F7, 0x0ED, 0x0FF, 0x0F8,
    0x0F0, 0x0FF, 0x0F8, 0x0F4, 0x0FF, 0x0F9, 0x0ED, 0x0FF, 0x0FA, 0x0F0, 0x0FF,
    0x0FB, 0x0F4, 0x0FF, 0x0FB, 0x0ED, 0x0FF, 0x0FD, 0x0F0, 0x0FF, 0x0FF, 0x0F4)



sendDataA = (
    (0x491, [2, 0xEB, 0x91]),
    (0x491, [9, 0xF0, 0xEF]),
    (0x492, [0xF9, 0xFF]),
    (0x492, [0xF8, 0x19]),
)

sendDataB = (
    (0x491, [2, 0xEB, 0x96]),
    (0x491, [0x0E, 0x10, 0x0F]),
    (0x492, [0x11, 0x0F]),
    (0x492, [0x12, 0x0F]),
    (0x492, [0x13, 0x0F]),
    (0x492, [0x14, 0x0F]),
    (0x492, [0x15, 0x0F]),
    (0x492, [0x16, 0x0F]),
    (0x492, [0x17, 0x0F]),
    (0x492, [0x18, 0x0F]),
)

sendDataC = (
    (0x491, [0x0F, 0xFF, 0x00]),
    (0x492, [0x9D, 0x00]),
    (0x492, [0x9B, 0x00]),
    (0x491, [0x0F, 0xFF, 0x02]),
    (0x492, [0x30, 0x00]),
    (0x492, [0x33, 0x00]),
    (0x491, [0x0E, 0x80, 0x90]),
    (0x491, [0x02, 0x7F, 0x01]),
    (0x491, [0x07, 0xFF, 0x04]),
)

sendDataC_cc5False = (
    (0x491, [0x0F, 0xFF, 0x00]),
    (0x492, [0x9D, 0x00]),
    (0x492, [0x9B, 0x00]),
    (0x491, [0x0E, 0x80, 0x90]),
    (0x491, [0x02, 0x7F, 0x01]),
    (0x491, [0x07, 0xFF, 0x04]),
)

sendDataD = (
    (0x492, [0x10, 0x0]),
    (0x492, [0x11, 0x0]),
    (0x492, [0x12, 0x0]),
    (0x492, [0x13, 0x0]),
    (0x492, [0x14, 0x0]),
    (0x492, [0x15, 0x0]),
    (0x492, [0x16, 0x0]),
    (0x492, [0x17, 0x0]),
    (0x492, [0x18, 0x0]),
    (0x492, [0x19, 0x0]),
    (0x492, [0x1A, 0x0]),
    (0x492, [0x1B, 0x0]),
    (0x492, [0x1C, 0x0]),
    (0x492, [0x1D, 0x0]),
    (0x492, [0x1E, 0x0]),
    (0x492, [0x1F, 0x0]),
    (0x492, [0x20, 0x0]),
    (0x492, [0x21, 0x0]),
    (0x492, [0x22, 0x0]),
    (0x492, [0x23, 0x0]),
    (0x492, [0x24, 0x0]),
    (0x492, [0x25, 0x0]),
    (0x492, [0x26, 0x0]),
    (0x492, [0x27, 0x0]),
    (0x492, [0x28, 0x0]),
    (0x492, [0x29, 0x0]),
    (0x492, [0x2A, 0x0]),
    (0x492, [0x2B, 0x0]),
    (0x492, [0x2C, 0x0]),
    (0x492, [0x2D, 0x0]),
    (0x492, [0x2E, 0x0]),
    (0x492, [0x2F, 0x0]),
    (0x492, [0x30, 0x0]),
)

sendDataE = (
    (0x492, (0x32, 0x01)),
)

sendDataColorProfile = (
    (0x491, [0x0D, 0, 0]),
    (0x492, [1, 0]),
    (0x492, [2, 0]),
    (0x492, [3, 0]),
    (0x492, [4, 0]),
    (0x492, [5, 0]),
    (0x492, [6, 0]),
    (0x492, [7, 0]),
    (0x492, [8, 0]),
    (0x492, [9, 0]),
    (0x492, [0x0A, 0]),
    (0x492, [0x0B, 0]),
    (0x492, [0x0C, 0]),
    (0x492, [0x0D, 0]),
    (0x492, [0x0E, 0]),
    (0x492, [0x0F, 0]),
    (0x492, [0x10, 0]),
    (0x492, [0x11, 0]),
    (0x492, [0x12, 0]),
    (0x492, [0x13, 0]),
    (0x492, [0x14, 0]),
    (0x492, [0x15, 0]),
    (0x492, [0x16, 0]),
    (0x492, [0x17, 0]),
    (0x492, [0x18, 0]),
    (0x492, [0x19, 0]),
    (0x492, [0x1A, 0]),
    (0x492, [0x1B, 0]),
    (0x492, [0x1C, 0]),
    (0x492, [0x1D, 0]),
    (0x492, [0x1E, 0]),
    (0x492, [0x1F, 0]),
    (0x492, [0x20, 0]),
    (0x492, [0x21, 0]),
    (0x492, [0x22, 0]),
    (0x492, [0x23, 0]),
    (0x492, [0x24, 0]),
    (0x492, [0x25, 0]),
    (0x492, [0x26, 0]),
    (0x492, [0x27, 0]),
    (0x492, [0x28, 0]),
    (0x492, [0x29, 0]),
    (0x492, [0x2A, 0]),
    (0x492, [0x2B, 0]),
    (0x492, [0x2C, 0]),
    (0x492, [0x2D, 0]),
    (0x492, [0x2E, 0]),
    (0x492, [0x2F, 0]),
    (0x492, [0x30, 0]),
    (0x492, [0x31, 0]),
    (0x492, [0x32, 0]),
    (0x492, [0x33, 0]),
    (0x492, [0x34, 0]),
    (0x492, [0x35, 0]),
    (0x492, [0x36, 0]),
    (0x492, [0x37, 0]),
    (0x492, [0x38, 0]),
    (0x492, [0x39, 0]),
    (0x492, [0x3A, 0]),
    (0x492, [0x3B, 0]),
    (0x492, [0x3C, 0]),
    (0x492, [0x3D, 0]),
    (0x492, [0x3E, 0]),
    (0x492, [0x3F, 0]),
    (0x492, [0x40, 0]),
    (0x492, [0x41, 0]),
    (0x492, [0x42, 0]),
    (0x492, [0x43, 0]),
    (0x492, [0x44, 0]),
    (0x492, [0x45, 0]),
    (0x492, [0x46, 0]),
    (0x492, [0x47, 0]),
    (0x492, [0x48, 0]),
    (0x492, [0x49, 0]),
    (0x492, [0x4A, 0]),
    (0x492, [0x4B, 0]),
    (0x492, [0x4C, 0]),
    (0x492, [0x4D, 0]),
    (0x492, [0x4E, 0]),
    (0x492, [0x4F, 0]),
    (0x492, [0x50, 0]),
    (0x492, [0x51, 0]),
    (0x492, [0x52, 0]),
    (0x492, [0x53, 0]),
    (0x492, [0x54, 0]),
    (0x492, [0x55, 0]),
    (0x492, [0x56, 0]),
    (0x492, [0x57, 0]),
    (0x492, [0x58, 0]),
    (0x492, [0x59, 0]),
    (0x492, [0x5A, 0]),
    (0x492, [0x5B, 0]),
    (0x492, [0x5C, 0]),
    (0x492, [0x5D, 0]),
    (0x492, [0x5E, 0]),
    (0x492, [0x5F, 0]),
    (0x492, [0x60, 0]),
    (0x492, [0x61, 0]),
    (0x492, [0x62, 0]),
    (0x492, [0x63, 0]),
    (0x492, [0x64, 0]),
    (0x492, [0x65, 0]),
    (0x492, [0x66, 0]),
    (0x492, [0x67, 0]),
    (0x492, [0x68, 0]),
    (0x492, [0x69, 0]),
    (0x492, [0x6A, 0]),
    (0x492, [0x6B, 0]),
    (0x492, [0x6C, 0]),
    (0x492, [0x6D, 0]),
    (0x492, [0x6E, 0]),
    (0x492, [0x6F, 0]),
    (0x492, [0x70, 0]),
    (0x492, [0x71, 0]),
    (0x492, [0x72, 0]),
    (0x492, [0x73, 0]),
    (0x492, [0x74, 0]),
    (0x492, [0x75, 0]),
)

