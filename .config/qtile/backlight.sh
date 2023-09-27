#!/bin/bash

set -eo pipefail

method="$1"
v="$2"

c=$(xrandr --current --verbose | grep eDP-1 -A5 | tail -1 | awk '{print $2}')

if [ "$method" = "inc" ]; then
  result=$(echo "$c + 0.${v}" | bc)
else
  result=$(echo "$c - 0.${v}" | bc)
fi

if (( $(echo "$c <= $v" | bc -l) )); then
  result="0$result"
fi

xrandr --output eDP-1 --brightness "$result"
