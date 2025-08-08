#!/bin/bash
#set-up for single machine or cluster based execution
. ./cmd.sh
#set the paths to binaries and other executables
[ -f path.sh ] && . ./path.sh


# Author : Abhishek Dey


kaldi_path=$1
base_path=$2
n_gram=$3


#kaldi_path='/opt/kaldi'
#base_path='/home/developer/egs/ad_assamese_asr'
#n_gram=2 # for bigram set n_gram=2 for tri_gram set n_gram=3


irlstm_path="$kaldi_path/tools/irstlm"
lm_arpa_path=$base_path/data/local/lm
train_dict=dict
train_lang=lang_bigram
train_folder=train


#==================================================================================

while read line

do

echo "<s> $line </s>" >> $base_path/data/$train_folder/lm_train.txt

done < $base_path/data/$train_folder/trans


#==================================================================================


echo ============================================================================
echo "                   Creating Training bigram LM               	        "
echo ============================================================================



rm -rf $base_path/data/local/$train_dict/lexiconp.txt $base_path/data/local/$train_lang $base_path/data/local/tmp_$train_lang $base_path/data/$train_lang

mkdir -p $base_path/data/local/tmp_lang_bigram


utils/prepare_lang.sh --num-sil-states 3 data/local/$train_dict '!SIL' data/local/$train_lang data/$train_lang

$irlstm_path/bin/build-lm.sh -i $base_path/data/$train_folder/lm_train.txt -n $n_gram -o $base_path/data/local/tmp_lang_bigram/lm_phone_bg.ilm.gz

gunzip -c $base_path/data/local/tmp_lang_bigram/lm_phone_bg.ilm.gz | utils/find_arpa_oovs.pl data/$train_lang/words.txt  > data/local/tmp_lang_bigram/oov.txt

gunzip -c $base_path/data/local/tmp_$train_lang/lm_phone_bg.ilm.gz | grep -v '<s> <s>' | grep -v '<s> </s>' | grep -v '</s> </s>' | grep -v 'SIL' | $kaldi_path/src/lmbin/arpa2fst - | fstprint | utils/remove_oovs.pl data/local/tmp_$train_lang/oov.txt | utils/eps2disambig.pl | utils/s2eps.pl | fstcompile --isymbols=data/$train_lang/words.txt --osymbols=data/$train_lang/words.txt --keep_isymbols=false --keep_osymbols=false | fstrmepsilon > data/$train_lang/G.fst 

$kaldi_path/src/fstbin/fstisstochastic data/$train_lang/G.fst 


echo ============================================================================
echo "                   End of Script             	        "
echo ============================================================================
