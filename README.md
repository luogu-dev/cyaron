# Project CYaRon
CYaRon: Yet Another Random Olympic-iNformatics test data generator

By Luogu
[![](https://travis-ci.org/luogu-dev/cyaron.svg?branch=master)](https://travis-ci.org/luogu-dev/cyaron)

你是否遇到以下情况：
- 希望在5分钟内写出一组随机数据
- 希望生成一个合适的随机图或者树，且有一定强度
- 希望生成一组随机数列或者向量，且不能重复。

那么，你可以借助CYaRon和Python，来快速生成一组数据。目前支持的特性有：

- 建一个随机图（简单图或者非简单图，有向图或无向图，带权图或者无权图）
- 建一个随机树（链状、随机树、或者菊花图，而且可以设定树的强弱）
- 生成一组允许相同或者互相不同的多维向量（可以较快速度生成10^6组、范围到10^9的向量或者数列）
- 根据函数解析式生成数列
- 生成一些随机多边形，并且可以求面积、周长等
- 从字典生成随机字符串、单词、句子、段落

**快速上手指南**

你可以下载github源代码  https://github.com/luogu-dev/cyaron ，或者`pip install cyaron`。在此之前，需要准备好python2/3。

[文档](https://github.com/luogu-dev/cyaron/wiki/%E9%A6%96%E9%A1%B5)仍在建设中，尚不完整，之后将慢慢补充。请根据`examples`和源代码进行YY。

首批贡献者 @fjzzq2002 @lin_toto @kkksc03 

之后计划实现云Generator，即只需提供写好的python脚本以及std，上传到服务器，即可下载一个测试数据的压缩包，真正实现5分钟生成一个测试数据！

目前CYaRon的功能还比较初级，希望各位大佬一起来协助改进这个项目。希望这个项目可以帮助大家节省时间！
