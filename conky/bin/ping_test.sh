#!/bin/bash
if ping -c 1 -W 1 -nq $1 > /dev/null; then
	echo "Up"
else
	echo "Down"
fi
