#!/bin/bash

#picom &
#nm-applet &

dunst &

find ~/.xwallpapers -type f | shuf -n 1 | xargs xwallpaper --stretch
