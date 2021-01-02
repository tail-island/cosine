#!/bin/sh

for i in 1 2 3 4 5 6
do
    echo phase-${i}
    cd phase-${i}

    ./check

    cd ..
done
