#!/usr/bin/python3
#
#    exploreValue.py           (C) 2022-2023, Aurélien Croc (AP²C)
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

def setAmpGainMute(v) :
    concerned = []
    if v & 0x8000 :
        if v & 0x4000 :
            concerned.append("in/out amp")
        else :
            concerned.append("out amp")
    elif v & 0x4000 :
        concerned.append("in amp")
    if v & 0x2000 :
        if v & 0x1000 :
            concerned.append("stereo channel")
        else :
            concerned.append("left channel")
    elif v & 0x1000 :
        concerned.append("right channel")

    idx = (val & 0x0F00) >> 8
    mute = "true" if val & 0x0080 else "false"
    gain = val & 0x007F
    print("%s: idx=%i, muted=%s, gain=%i" % (', '.join(concerned), idx, mute, gain))
    
def getAmpGainMute(v) :
    mute = "true" if val & 0x0080 else "false"
    gain = val & 0x007F
    print("muted=%s, gain=%i" % (mute, gain))

def setPinCtl(v) :
    hphn = "enabled" if val & 0x80 else "disabled"
    out = "enabled" if val & 0x40 else "disabled"
    inE = "enabled" if val & 0x20 else "disabled"
    rsvd = (val & 0x18) >> 3
    vrefen = val & 0x7
    if vrefen == 0 :
        vrefen = "Hi-Z"
    elif vrefen == 1 :
        vrefen = "50%"
    elif vrefen == 2 :
        vrefen = "Ground"
    elif vrefen == 4 :
        vrefen = "80%"
    elif vrefen == 5 :
        vrefen = "100%"
    else :
        vrefen = "reserved"
    print("low impedence amplifier=%s, out=%s, in=%s, VRef=%s, rsvd=%i" % (hphn, out, inE, vrefen, rsvd))
    
def unsolEnabled(v) :
    isEnabled = "enabled" if v & 0x80 else "disabled"
    tag = v & 0x3F
    print("Unsol response: %s, tag=%i" % (isEnabled, tag))

def eapdBtl(v) :
    lrSwap = "true" if v & 0x04 else "false"
    eapd = "true" if v & 0x02 else "false"
    btl = "true" if v & 0x01 else "false"
    print("L/R swap=%s, EAPD=%s, BTL=%s" % (lrSwap, eapd, btl))

def streamFormat(v) :
    stype = "non-PCM" if v & 0x8000 else "PCM"
    baseRate = "44,1 KHz" if v & 0x4000 else "48 KHz"
    rateMultiplier = (v & 0x3800) >> 11
    if rateMultiplier == 0 :
        rateMultiplier = '1'
    elif rateMultiplier == 1 :
        rateMultiplier = 'x2'
    elif rateMultiplier == 2 :
        rateMultiplier = 'x3'
    elif rateMultiplier == 3 :
        rateMultiplier = 'x4'
    else :
        rateMultiplier = 'unknown'
    rateDivisor = '/' + str(((v & 0x0700) >> 8) + 1)
    bps = (v & 0x0070) >> 4
    if bps == 0 :
        bps = '8-Bits'
    elif bps == 1 :
        bps = '16-Bits'
    elif bps == 2 :
        bps = '20-Bits'
    elif bps == 3 :
        bps = '24-Bits'
    elif bps == 4 :
        bps = '32-Bits'
    else :
        bps = 'reserved'
    channels = (v & 0x000F) + 1
    print("stream type=%s, base rate=%s, rate multiplier=%s, rate divisor=%s, bits per sample=%s, nr channels=%i" % \
        (stype, baseRate, rateMultiplier, rateDivisor, bps, channels))

portConnValue = (
    'jack',
    'no physical connection',
    'fixed function device',
    'both jack and internal device',)
locationValue = (
    ('external', ('N/A', 'rear', 'front', 'left', 'right', 'top', 'bottom', 'rear panel', 'drive bay', '?')),
    ('internal', ('N/A', '?', '?', '?', '?', '?', '?', 'chassis', 'digital display', 'ATAPI')),
    ('separate chassis', ('N/A', 'rear', 'front', 'left', 'right', 'top', 'bottom', '?', '?', '?')),
    ('other', ('N/A', '?', '?', '?', '?', '?', 'bottom', 'mobile lid inside', 'mobile lid outside', 'ATAPI')))
defaultDeviceValue = (
	'line out',
	'speaker',
	'HP out',
	'CD',
	'SPDIF out',
	'digital other out',
	'modem line side',
	'modem handset side',
	'line in',
	'AUX',
	'mic in',
	'telephony',
	'digital other in',
	'???',
	'other')
connectionTypeValue = (
	'unknown',
	'1/8" stereo/mono',
	'1/4" stereo/mono',
	'ATAPI internal',
	'RCA',
	'optical',
	'other digital',
	'other analog',
	'multichannel analog (DIN)',
	'XLR/professional',
	'RJ-11 (modem)',
	'combination',
	'other')
colorValue = (
	'unknown',
	'black',
	'grey',
	'blue',
	'green',
	'red',
	'orange',
	'yellow',
	'purple',
	'pink',
	'reserved',
	'white',
	'other')
def pinConfig(v) :
    portConn = (val >> 30) & 0x3
    location = (val >> 24) & 0x3F
    defDev = (val >> 20) & 0xF
    connType = (val >> 16) & 0xF
    color = (val >> 12) & 0xF
    misc = (val >> 8) & 0xF
    defAssoc = (val >> 4) & 0xF
    seq = val & 0xF

    portConn = portConnValue[portConn]
    v = (location >> 4) & 0x3
    loc = location & 0xF
    (t, l) = locationValue[(location >> 4) & 0x4]
    if loc < 0xA :
        location = t + ' ' + l[loc]
    else :
        location = t + ' reserved'
    defDev = defaultDeviceValue[defDev]
    connType = connectionTypeValue[connType]
    color = colorValue[color]
    jdo = 'true' if misc & 0x1 else 'false'
    print('port=%s, location=%s, default device=%s, connection type=%s, color=%s, jack detection override=%s, default assoc=%x, seq=%x' % (portConn, location, defDev, connType, color, jdo, defAssoc, seq))

def getPinSense(v) :
    presence = 'true' if v & 0x80000000 else 'false'
    eldValid = 'true' if v & 0x40000000 else 'false'
    impedenceValue = v & 0x7FFFFFFF

    print('presence=%s, [digital] ELD valid=%s, [analogic] impedence '
        'value=0x%x' % (presence, eldValid, impedenceValue))

if len(sys.argv) < 3 :
    print("Usage: %s <type> <val>" % sys.argv[0])
    print("Types:")
    print("  sam = set amp gain/mute")
    print("  gam = get amp gain/mute")
    print("  spc = set pin ctl")
    print("  ue = unsol enabled")
    print("  eb = EAPD/BTL")
    print("  sf = set stream format")
    print("  pc = pin configuration")
    print("  gps = get pin sense")
    sys.exit(0)

val = int(sys.argv[2], base=16)
t = sys.argv[1]
if t == 'sam' :
    setAmpGainMute(val)
elif t == 'gam' :
    getAmpGainMute(val)
elif t == 'spc' :
    setPinCtl(val)
elif t == 'ue' :
    unsolEnabled(val)
elif t == 'eb' :
    eapdBtl(val)
elif t == 'sf' :
    streamFormat(val)
elif t == 'pc' :
    pinConfig(val)
elif t == 'gps' :
    getPinSense(val)
else :
    print("Type unknown")

