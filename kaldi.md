
# Kaldi Installation Steps:

**Author: Abhishek Dey**

## Method 1. Using Docker image

* Based on your CUDA and NVIDIA-Driver versions, Pull docker image from [docker hub](https://hub.docker.com/r/kaldiasr/kaldi/tags)


```
docker pull kaldiasr/kaldi:gpu-ubuntu20.04-cuda11-2024-12-02

```

* Docker run

```

docker run --gpus 0 -e NVIDIA_VISIBLE_DEVICES=0 --shm-size 4G -it --rm -v $PWD:/home/developer kaldiasr/kaldi:gpu-ubuntu20.04-cuda11-2024-12-02

```

## Install sgmm binaries

### cd kaldi/src/sgmm2

```

make

```

### cd kaldi/src/sgmm2bin

```
make

```

## Method 2. Using github repository clone

```
git clone https://github.com/kaldi-asr/kaldi

```

### Install dependent libraries

```
sudo apt-get update
sudo apt-get install libblas-*
sudo apt-get install automake
sudo apt-get install libtool-*
sudo apt-get install libatlas-*
sudo apt-get install zlib1g-dev
sudo apt-get install g++-multilib
sudo apt-get install git
sudo apt-get install gawk


```


### cd kaldi/tools

* To check the prerequisites for Kaldi, first run

```
extras/check_dependencies.sh

```

* Install dependencies if not pre-installed

```
sudo apt-get install sox gfortran

extras/install_mkl.sh

```

**NOTE:**

* As of current date, the **make** script looks for open-fst 1.8.4 but the link is not working

* In that case,  change version of openfst in make file from **1.8.4** to **1.7.9**

```

Replace : OPENFST_VERSION ?= 1.8.4

To      : OPENFST_VERSION ?= 1.7.9


```

* OpenFST Links:

[Open-fst link](https://www.openfst.org/twiki/bin/view/FST/FstDownload)

[Open-slr link](https://openslr.org/2/)


* Once dependencies are installed, run **make** followed by 

```
make

```

* Install irstlm and srilm

```
extras/install_irstlm.sh

extras/install_srilm.sh

```

### cd kaldi/src

```
./configure --shared

make depend -j 4

make -j 4

```

## Install sgmm binaries

### cd kaldi/src/sgmm2

```

make

```

### cd kaldi/src/sgmm2bin

```
make

```

