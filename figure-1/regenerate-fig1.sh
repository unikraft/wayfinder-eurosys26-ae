#!/bin/bash

OUTPUT=results.csv

# clone Linux
echo "Cloning Linux ..."
git clone https://github.com/torvalds/linux.git

# Count Kconfig option for each tag
echo "Counting Kconfig options for each tag ..."
cd linux
git checkout master

echo "" > $OUTPUT
for t in `git tag --sort=-taggerdate`; do
    git checkout  $t &> /dev/null
    options=`grep -E -RnIs "^config\s[A-Z_0-9]+$" . | wc -l`
    date=`git log -1 --format="%at" | xargs -I{} date -d @{} +%Y/%m/%d_%H:%M:%S`
    echo "$date $t $options" >> $OUTPUT
done

mv $OUTPUT ..
cd -

# Plot graph
./plot.py
