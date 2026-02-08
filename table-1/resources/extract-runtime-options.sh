#!/bin/bash

number_check_re='^[0-9]+$'

if [ ! $# == "1" ]; then
	echo "usage: $0 /proc/sys/path/to/subfolder"
	exit
fi

# Filter only files that are writable
for option in `find $1 -maxdepth 1 -type f -perm /222 -printf "%f\n"`; do
	default_val=`cat $1/$option`
	echo "- $option:"
	echo "  - path: $1/$option"

    # Dumb inference of the type: if it's 1 or 0 it's a bool, if it's something
    # else but a number it's an int, and if it's somehting else it's a list.
	if [[ $default_val == "0" || $default_val == "1" ]]; then
		echo "  - type: bool"
	elif [[ $default_val =~ $number_check_re ]]; then
		echo "  - type: int"
	else
		echo "  - type: list"
        echo "  - values: [ TODO ]"
	fi

	echo "  - default: $default_val"
done
