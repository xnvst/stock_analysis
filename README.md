# stock_analysis

## installation dependencies

### 1. anaconda

1.1
wget  https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
bash  Anaconda3-2019.03-Linux-x86_64.sh
sudo vim ~/.bashrc
export PATH="/home/user/anaconda3/bin:$PATH"
source ~/.bashrc

1.2
mkdir -p ~/mywork && cd ~/mywork
jupyter notebook

---------------------------------------------------------------------

### 2. ta-lib:
http://mrjbq7.github.io/ta-lib/index.html

2.1. Dependencies
Linux
Download ta-lib-0.4.0-src.tar.gz and:

$ untar and cd
$ ./configure --prefix=/usr
$ make
$ sudo make install

2.2. install Lib
pip install TA-Lib

---------------------------------------------------------------------

### 3. alpha_vantage

---------------------------------------------------------------------


---------------------------------------------------------------------


---------------------------------------------------------------------

## todo-list
0. read data according to date range (compact) ---------------done
1. collect data ---------------done

2. pattern recognition for given period of time (technical analysis)
2.1 ---------------candle stick done
2.2 talib
2.3 given time

3. candle stick plot better

4. news feed (基本面 & 板块分析)

5. ML

6. 懒人炒股心经


## reference

https://github.com/HuaRongSAO/talib-document

https://www.quantopian.com