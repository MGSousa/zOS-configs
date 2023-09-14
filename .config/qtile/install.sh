#!/bin/sh

echo "Installing first xcffib, cairocffi then qtile"
pip install 'xcffib >= 0.10.1' && \
pip install --no-cache-dir 'cairocffi >= 0.9.0' && \
pip install qtile psutil dbus-next

# FIX qtile lib on new versions of python
pip install --no-build-isolation git+https://github.com/qtile/qtile
