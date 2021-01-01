#!/bin/sh

for i in 1 2 3 4 5 6
do
    echo phase-${i}
    cd phase-${i}

    python create_table.py > netkeiba.tsv
    ./train
    ./check

    cd ..
done
