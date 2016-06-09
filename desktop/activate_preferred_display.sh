#!/bin/sh

# For a laptop: Enable only the external display if it is
# connected, otherwise enable only the internal display.

INTERNAL="eDP1"
EXTERNAL="DP2"

if (xrandr | grep "$EXTERNAL connected"); then
    xrandr --output $INTERNAL --off --output $EXTERNAL --auto
else
    xrandr --output $INTERNAL --auto --output $EXTERNAL --off
fi
