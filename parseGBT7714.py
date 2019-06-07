#!/bin/python3

# -*- coding: utf-8 -*-
#==============================
#    Author: Elun Dai
#    Last modified: 2019-06-07 15:24
#    Filename: parse7714.py
#    Description:
#    
#=============================#
import re
from collections import defaultdict

useras = {
    'J' : ['author.title[usera].translator,year,volume(number):pages[urldate].url.doi',
           'author.title[usera].translaotr,year,volume(number):pages.url',
           'author.title[usera].title,year,volume(number):pages.url'],
    "M" : ['author.tittle[usera].tittle[usera].location:publisher'],
    'R' : ['author.title[usera].location:publisher,date.',
           'author.title:subtittle[usera].location:publisher,date.',],
}

entrytypes = {
    'J' : 'article',
    'R' : 'report',
}

for usera in useras:
    useras[usera].sort(key=len, reverse=True)

def str2pattern(s):
    pattern = s
    pattern = re.sub(r'\.', r'\.', pattern)
    pattern = re.sub(r'\[', r'\[', pattern)
    pattern = re.sub(r'\]', r'\]', pattern)
    pattern = re.sub(r'\(', r'\(', pattern)
    pattern = re.sub(r'\)', r'\)', pattern)
    pattern = re.sub(r'\w+', '(.*?)', pattern)
    files = re.findall(r'\w+', s)
    return pattern, files

def delspace(s):
    s = re.sub(r'^ *\[\d+\] *', r'',s.strip())
    s = re.sub(r' *([\.,\[\]\(\):]) *', r'\1',s)
    return s

def getusera(s):
    res = re.findall(r'\[(.*)\]', s)
    if res is not None:
        return res[0]
    else:
        return None

def parse(s):
    parsed_dict = defaultdict(str)
    s = delspace(s)
    parsed_dict['source'] = s
    print("parsing", s)
    usera = getusera(s)
    parsed_dict['usera'] = usera
    for style in useras.get(usera):
        pattern, files = str2pattern(style)
        res = re.match(pattern, s)
        if res is not None:
            res = res.groups()
            assert len(files) == len(res)
            parsed_dict.update(dict(zip(files, res)))
            break
    print("matched!", style)
    print(len(parsed_dict)-1, "files has found!")
    return parsed_dict

def genbib(parsed_dict):
    bib = '%{}\n'.format(parsed_dict.pop('source'))
    bib += "@%s{%s,\n" % (entrytypes[parsed_dict['usera']], re.sub(' ', '_', parsed_dict['title']))
    for key in parsed_dict:
        bib += '%s = {%s},\n' % (key, parsed_dict[key])
    bib = bib[:-2] + "\n}\n\n"
    return  bib

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Parse GB/T 7714 into bibtex style.')
    parser.add_argument("input",
                        metavar="<input>",
                        help="input GB/T 7714 filename")
    parser.add_argument("output",
                        metavar="<output>",
                        help="output bibtex filename")
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        lines = f.readlines()
    o = open(args.output, 'w')
    for line in lines:
        parsed_dict = parse(line)
        o.write(genbib(parsed_dict))
    o.close()
    print("writed to ", args.output)
