#!/bin/sh

echo "Installing first xcffib then cairocffi and finally qtile"
pip install 'xcffib >= 0.10.1' && \
pip install --no-cache-dir 'cairocffi >= 0.9.0' && \
pip install qtile psutil
