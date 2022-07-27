#!/bin/sh

ps aux --no-headers | sort -nk 3 | awk -F' ' '{print $3"% - MEM:" $4" << "$11}' | tail -1
