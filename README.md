中文文本自动纠错
====================
#### 原因：在做智能家居的声控启动的时候发现，声音命令转化为文字的时候有时候会有问题，例如天气预报 翻译成天汽预报，就想到了搜索引擎中的纠错功能,但是由于个人水平有限制，所以第一版本还不是很详细

# 开发语言
* python

# 如何使用
* python main.py

# 系统原理：
#### 围绕着如何找出这段文字中是否有错误的字？
* 找到了很多语料集，进行分词统计词频
* 将待分析的文字的每一个字拆开放到一个数组中
  * 计算每一个字是否在词频字典中有，如果有说明这个字是对的
  * 二元语言模型与字典分词相结合的方法，命令Ui=WiWi+1(就是字符i和字符i+1结合起来的字符串在词频字典中的词频),假设一个字i不对，则
  Ui=WiWi+1 ,Ui-1=Wi-1Wi Ui 和Ui-1都是0，说明这个词没有这种分词的存在，说明这次词是不对的

# 目录结构 

    ├── checkproof.py
    ├── chineseproofread.py
    ├── correct  正确的短语 需要自己收集
    ├── dicmap.txt  分词词频文件(需要语料集的可以找我)
    ├── __init__.py
    ├── main.py  主程序
    └── README.MD

# 参考文章
* java实现Google和Baidu的“您是不是要找”功能(http://www.cnblogs.com/wuren/archive/2013/01/16/2862873.html)
* PyLucene实战(http://www.open-open.com/lib/view/open1347377559257.html)

# How to Contact
#### QQ:36405410
#### Email:apanly@163.com

# Copying
#### Free use of this software is granted under the terms of the GNU Lesser General Public License (LGPL)
