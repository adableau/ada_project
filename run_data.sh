#!/usr/bin/env bash

set -e
set -x

# move data Task
solver_task() {
    local datadir=$1
    local model=$2
    if [ ! -e ./data ]; then
        mkdir data
    else
        rm -rf ./data
        mkdir data
    fi

    cat ./dataset/${datadir}/train.txt | awk -F '\t' '{_[$1]=1; _[$3]=1}END{i=0; for (v in _){print v, i; i++}}' > ./data/entity2id.txt
    cat ./dataset/${datadir}/train.txt | awk -F '\t' '{_[$2]=1;}END{i=0; for (v in _){print v, i; i++}}' > ./data/relation2id.txt
    cat ./dataset/${datadir}/train.txt | awk -F '\t' '{print $1, $3, $2}' > ./data/train.txt
    cp ./dataset/${datadir}/test.txt ./data/test.txt

    clang++ -std=c++0x -O2 Train_${model}.cpp -o Train_${model} && ./Train_${model}

    cp entity2vec.bern models/entity2vec_${datadir}.bern
    cp relation2vec.bern models/relation2vec_${datadir}.bern
    mv entity2vec.bern data/
    mv relation2vec.bern data/

    python task1.py ./data/entity2vec.bern \
        ./data/relation2vec.bern \
        ./data/entity2id.txt \
        ./data/relation2id.txt \
        ./data/test.txt > result/${datadir}.txt
}

solver_task2 FB_B TransE


