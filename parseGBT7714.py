#!/bin/python3

# -*- coding: utf-8 -*-
#==============================
#    Author: Elun Dai
#    Last modified: 2019-06-25 21:21
#    Filename: parseGBT7714.py
#    Description:
#=============================#
import re
from collections import defaultdict

useras = {
    'J' : ['author.title[usera].translator,year,volume(number):pages[urldate].url.doi.',
           'author.title[usera].translator,year,volume(number):pages.url.',
           'author.title[usera].translator,year,volume(number):pages.'],
    'M' : ['author.title[usera].location:publisher.',
           'author.title[usera].location:publisher,year:pages,volume.'],
    'R' : ['author.title[usera].location:publisher,date.',
           'author.title:subtitle[usera].location:publisher,date.'],
    'EB' : ['author.title[usera].url,date.',
                'author.title[usera].url,date/urldate.',],
    'N' : ['author.title[usera].journaltitle,date(number).',],
    'D' : ['author.title[usera].address:publisher,year.'],
    'C' : ['author.title.edition[usera].location:publisher,year:pages.'],
}

entrytypes = {
    'M' : 'book',
    'J' : 'article',
    'C' : 'proceedings',
    'G' : 'collection',
    'N' : 'newspaper',
    'D' : 'mastersthesis',
    'R' : 'report',
    'EB' : 'online',
    'S' : 'standard',
    'P' : 'patent',
    'DB' : 'database',
    'CP' : 'software',
    'A' : 'archive',
    'CM' : 'map',
    'DS' : 'dataset',
    'Z' : 'misc',
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
    s = re.sub(r'EB/OL', r'EB', s)
    res = re.findall(r'\[(.*?)\]', s)
    if res is not None:
        for usera in res:
            if usera in useras.keys():
                res = usera
                return res
    raise KeyError('Could not find pattern for usera ' + str(res) + ', plese add it manually to useras dictionary.')

def parse(s):
    parsed_dict = defaultdict(str)
    s = delspace(s)
    parsed_dict['source'] = s
    print("parsing", s)
    usera = getusera(s)
    styles = useras.get(usera)
    if styles is None:
        raise IndexError("Couldn't find pattern of entry file " + usera)
    for style in styles:
        pattern, files = str2pattern(style)
        res = re.match(pattern, s)
        if res is not None:
            res = res.groups()
            assert len(files) == len(res)
            parsed_dict.update(dict(zip(files, res)))
            parsed_dict['author'] = re.sub(r',', r' and ', parsed_dict['author']) # use 'and' to seperate authors
            parsed_dict['usera'] = usera
            print("matched!", style)
            print(len(parsed_dict)-1, "entry files has found!")
            return parsed_dict
    return None

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

    failed = list()
    with open(args.input, 'r') as f:
        lines = f.readlines()
    o = open(args.output, 'w')
    for line in lines:
        parsed_dict = parse(line)
        if parsed_dict is not None:
            o.write(genbib(parsed_dict))
        else:
            failed.append(line)
    o.close()
    print("writed to", args.output)

    if len(failed) > 0:
        print("failed to parse:")
        for i in failed:
            print('\t',i)
