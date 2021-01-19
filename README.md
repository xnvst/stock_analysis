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

2. analysis
2.1 candle stick pattern ---------------done
2.2 technical analysis: MACD & PV(price-volume) ---------------done
2.3 intra-day (TBD)

3. candle stick plot better ---------------done

4. news feed (基本面 & 板块分析 & 机构持仓 & 资金流入)
4.1 目前人工进行 (yahoo, fintel, finviz, youtube, futu, tiprank)
4.2 ML (investigation)

5.
5.1 draw chart according to symbol ---------------done
5.2 futu api: 资金流入 etc. ---------------in progress

6. 懒人炒股心经 (TBD)

Steven:
----1,学价量关系 2，趋势判断 3，盘口语言 4，机构做庄方法 （建仓吸筹， 洗盘， 拉升，出货）5，压力支撑判断
----选票基础价量关系，K线位阶，图形结构，资金辅助增加胜率，先考虑大资金的态度，再看中小资金是否跟风


## reference

https://github.com/RomelTorres/alpha_vantage

https://github.com/HuaRongSAO/talib-document

https://www.quantopian.com