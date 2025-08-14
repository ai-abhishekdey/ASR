#!/bin/bash


lang_dir=$1
vocab_size=$2

python3 local/train_bpe_model.py --lang-dir $lang_dir --vocab-size $vocab_size --transcript $lang_dir/transcript_words.txt

python3 local/prepare_lang_bpe.py --lang-dir $lang_dir

python3 local/validate_bpe_lexicon.py --lexicon $lang_dir/lexicon.txt  --bpe-model $lang_dir/bpe.model


### Converting L.pt to L.fst

python3 shared/convert-k2-to-openfst.py --olabels aux_labels  $lang_dir/L.pt $lang_dir/L.fst

### Converting L_disambig.pt to L_disambig.fst

python3 shared/convert-k2-to-openfst.py --olabels aux_labels  $lang_dir/L_disambig.pt $lang_dir/L_disambig.fst

