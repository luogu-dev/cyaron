# Project CYaRon
CYaRon: Yet Another Random Olympic-iNformatics test data generator

By Luogu
[![](https://travis-ci.org/luogu-dev/cyaron.svg?branch=master)](https://travis-ci.org/luogu-dev/cyaron)

你是否遇到以下情况：
- 希望在5分钟内写出一组随机数据，并方便地使用它们对拍几个程序
- 希望生成一个合适的随机图或者树，且有一定强度
- 希望生成一组随机数列或者向量，且不能重复。

那么，你可以借助CYaRon和Python，来快速生成一组数据。目前支持的特性有：

- 建一个随机图（简单图或者非简单图，有向图或无向图，带权图或者无权图）
- 建一个随机树（链状、随机树、或者菊花图，而且可以设定树的强弱）
- 生成一组允许相同或者互相不同的多维向量（可以较快速度生成10^6组、范围到10^9的向量或者数列）
- 根据函数解析式生成数列
- 生成一些随机多边形，并且可以求面积、周长等
- 从字典生成随机字符串、单词、句子、段落

**使用范例**
```python
#!/usr/bin/env python

from cyaron import * # 引入CYaRon的库

_n = ati([0, 7, 50, 1E4]) # ati函数将数组中的每一个元素转换为整形，方便您可以使用1E4一类的数来表示数据大小
_m = ati([0, 11, 100, 1E4]) 

# 这是一个图论题的数据生成器，该题目在洛谷的题号为P1339
for i in range(1, 4): # 即在[1, 4)范围内循环，也就是从1到3
    test_data = IO(file_prefix="heat", data_id=i) # 生成 heat[1|2|3].in/out 三组测试数据

    n = _n[i] # 点数
    m = _m[i] # 边数
    s = randint(1, n) # 源点，随机选取一个
    t = randint(1, n) # 汇点，随机选取一个
    test_data.input_writeln(n, m, s, t) # 写入到输入文件里，自动以空格分割并换行

    graph = Graph.graph(n, m, weight_limit=5) # 生成一个n点，m边的随机图，边权限制为5
    test_data.input_writeln(graph) # 自动写入到输入文件里，默认以一行一组u v w的形式输出

    test_data.output_gen("D:\\std_binary.exe") # 标程编译后的可执行文件，不需要freopen等，CYaRon自动给该程序输入并获得输出作为.out
```

**快速上手指南**

你可以下载github源代码  https://github.com/luogu-dev/cyaron ，或者`pip install cyaron`。在此之前，需要准备好python2/3。

若您对Python不熟悉，可看[快速入门教程](https://github.com/luogu-dev/cyaron/wiki/Python-30%E5%88%86%E9%92%9F%E5%85%A5%E9%97%A8%E6%8C%87%E5%8D%97)。

[文档](https://github.com/luogu-dev/cyaron/wiki)已经大体完整，若有缺漏，请提出Issue并暂时根据`examples`和源代码进行YY。

首批贡献者 @fjzzq2002 @lin_toto @kkksc03 

之后计划实现云Generator，即只需提供写好的python脚本以及std，上传到服务器，即可下载一个测试数据的压缩包，真正实现5分钟生成一个测试数据！

目前CYaRon的功能还比较初级，希望各位大佬一起来协助改进这个项目。希望这个项目可以帮助大家节省时间！
