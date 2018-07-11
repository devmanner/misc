#!/bin/bash

PWD=$(dirname $(readlink -f $0))
BIN=$(dirname $PWD)/bin/is_linked.py

find $PWD \( -name '*.pptx' -o -name '*.xlsx' \) -exec $BIN -v {} \;

