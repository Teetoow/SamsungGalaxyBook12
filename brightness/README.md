# Samsung Galaxy book 12 brightness management

This directory contains a software which manages the brightness of the OLED screen of the Samsung Galaxy Book 12 computer.
Both versions of this software are avaiable: a C version and a python version. 
<i>Note that the python version is no more updated</i>.

The brightness management works pretty well except flickering which appears when brightness is below 40.

## Usage

1. Manually set the brightness:
    # brightness &lt;brightness value between 1 and 101&gt; [&lt;color profile&gt;]

2. Automatically set the brightness depending on the value of the brightness set  on the /sys directory (/sys/class/backlight/intel_backlight)

<i>This option is not available in the C code yet</i>
