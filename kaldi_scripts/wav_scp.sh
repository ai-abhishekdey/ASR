#!/bin/bash

wav_path=$1
utt_path=$2
out_path=$3


#wav_path=./data_src/wav
#utt_path=./data/test/utt
#out_path=./data/test/wav.scp



cat $utt_path | awk '{printf "%s\t%s%s%s\n",$1,"'$wav_path'/",$1,".wav"}' > $out_path


