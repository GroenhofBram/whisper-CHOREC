#!/usr/bin/env bash

INPUT_REF_CSV="./output/ref.csv"
INPUT_HYP_CSV="./output/hyp.csv"
# For overview of what each argument does see:
./sctk score --help
    
# !version=v0.3.0 && wget -q -O sctk https://github.com/shahruk10/go-sctk/releases/download/${version}/sctk && chmod +x ./sctk
!./sctk score \
    --ignore-first=true \
    --delimiter="," \
    --col-id=0 \
    --col-trn=1 \
    --cer=false \
    --out=./report \
    --ref=$INPUT_REF_CSV \
    --hyp=$INPUT_HYP_CSV \