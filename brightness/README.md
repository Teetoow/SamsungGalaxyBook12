# Samsung Galaxy book 12 brightness management

This directory contains a software which manages the brightness of the OLED screen of the Samsung Galaxy Book 12 computer.
Both versions of this software are avaiable: a C version and a python version. 
<i>Note that the python version is no more updated</i>.

The brightness management works pretty well except flickering which appears when brightness is below 40.

## Usage

1. Manually set the brightness:
```sh
# brightness <brightness value between 1 and 101> [<color profile>]
```

2. Automatically set the brightness depending on the value of the brightness set  on the /sys directory (/sys/class/backlight/intel_backlight)
```sh
# brightness watch [<color profile>]
```

Note that the color profile is a value between 0 and 6.
- 0 is the basic color profile
- 1 is for Cinema AMOLED profile
- 2 is for Photo AMOLED profile
- 3 is the adaptative profile [by default]
- 4 to 6 are other profiles not available from windows
