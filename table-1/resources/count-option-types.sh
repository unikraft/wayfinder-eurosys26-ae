#!/bin/bash

# Launch this script at the root of Linux's sources to count the number of
# kernel compile-time options of each type

for t in bool tristate string hex int; do
    total=0
    for f in `find . -name Kconfig`; do
        loc=`cat $f | grep "\s$t" | wc -l`
        let total="$total + $loc"
    done
    echo "$t: $total"
done
