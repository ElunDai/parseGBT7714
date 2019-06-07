# parseGBT7714

将GBT7714参考文献标准字符串转化为biblatex gb7714-2015格式的Python代码

# 使用方法

`python parseGBT7714.py <输入文件路径> <输出文件路径> `

**example**

```shell
python parseGBT7714.py test/input.txt test/out.bib
```



# 增加匹配规则

## 运行机制

在程序中可将文字版的匹配规则自动转化为正则表达式对输入字符串进行匹配，并将匹配结果写入到输出文件当中。

例如：`毛峡,丁玉宽.图像的情感特征分析及其和谐感评价[J].电子学报,2001,29(12A):1923-1927.`

首先会将规则`author.title[usera].translaotr,year,volume(number):pages.url`自动转化为正则表达式，`(.*?)\\.(.*?)\\[(.*?)\\]\\.(.*?),(.*?),(.*?)\\((.*?)\\):(.*?)\\.(.*?)`并将匹配到的结果输入到匹配规则所表示的bibtex引用域当中。其结果如下

```
@article{图像的情感特征分析及其和谐感评价,
pages = {1923-1927},
usera = {J},
number = {12A},
title = {图像的情感特征分析及其和谐感评价},
translaotr = {电子学报},
year = {2001},
volume = {29},
url = {},
author = {毛峡,丁玉宽}
}
```

## 自定义匹配规则

只需要修改源码中的文献类型`useras`这个字典变量内容即可，每一个文献类型对应一个列表的匹配规则。在执行匹配操作的时候会从长至短遍历这个列表并返回最先匹配到的结果.



**example**

连续出版物[J]类型：`[序号] 主要责任者．文献题名[J]．刊名，出版年份，卷号[期号]：起止页码．`

```
useras = {
    'J' : ['author.title[usera].translator,year,volume(number):pages[urldate].url.doi',
           'author.title[usera].translaotr,year,volume(number):pages.url'],
    "M" : ['author.tittle[usera].tittle[usera].location:publisher'],
    'R' : ['author.title[usera].location:publisher,date.',
           'author.title:subtittle[usera].location:publisher,date.'],
}
```



# bibtex file 域与中文对应

[参考gbt7714的github文档](https://github.com/CTeX-org/gbt7714-bibtex-style#%E6%96%87%E7%8C%AE%E7%B1%BB%E5%9E%8B)


|文献类型	|标识代码	|Entry Type|
| -----------| -----------|---|
|普通图书|M|book|
|图书的析出文献|M|incollection|
|会议录|C|proceedings|
|会议录的析出文献|C|inproceedings 或 conference|
|汇编|G|collection*|
|报纸|N|newspaper*|
|期刊的析出文献|J|article|
|学位论文|D|mastersthesis 或 phdthesis|
|报告|R|techreport|
|标准|S|standard*|
|专利|P|patent*|
|数据库|DB|database*|
|计算机程序|CP|software*|
|电子公告|EB|online*|
|档案|A|archive*|
|舆图|CM|map*|
|数据集|DS|dataset*|
|其他|Z|misc|

注：带 “*” 的类型不是 BibTeX 的标准文献类型。

|著录项目（域）|Entry Field|
| ----------- | -----------|
|主要责任者|author|
|题名|title|
|文献类型标识|mark*|
|载体类型标识|medium*|
|翻译者|translator*|
|编辑|editor|
|组织（用于会议）|organization|
|图书题名|booktitle|
|系列|series|
|期刊题名|journal|
|版本|edition|
|出版地|address|
|出版者|publisher|
|学校（用于phdthesis）|school|
|机构（用于techreport）|institution|
|出版年|year|
|卷|volume|
|期（或者专利号）|number|
|引文页码|pages|
|更新或修改日期|date*|
|引用日期|urldate*|
|获取和访问路径|url|
|数字对象唯一标识符|doi|
|语言|language*|
|拼音（用于排序）|key|

注:

- 其中带星号的不是 BibTeX/natbib 的标准著录项目。
- 不支持的 BibTeX 标准著录项目有 `annote`, `chapter`, `crossref`, `month`, `type`。
