#!/bin/bash

#picom &
#nm-applet &

find ~/.xwallpapers -type f | shuf -n 1 | xargs xwallpaper --stretch
