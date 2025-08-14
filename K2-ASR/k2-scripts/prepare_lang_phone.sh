#!/bin/bash


lang_dir=$1

### generate L_disambig.pt

python3 local/prepare_lang.py --lang-dir $lang_dir

### Converting L.pt to L.fst

python3 shared/convert-k2-to-openfst.py --olabels aux_labels  $lang_dir/L.pt $lang_dir/L.fst

### Converting L_disambig.pt to L_disambig.fst

python3 shared/convert-k2-to-openfst.py --olabels aux_labels  $lang_dir/L_disambig.pt $lang_dir/L_disambig.fst

