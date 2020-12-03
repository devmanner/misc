#!/bin/bash

while [ 1 ]; do
	for cmd in "$@"; do
		r=$(exec $cmd)
		rv=$?

		if [ $rv != 0 ]; then
			echo "$cmd returned not 0 ($rv) at "$(date)" with output:"
			echo $r
		fi
	done
done
