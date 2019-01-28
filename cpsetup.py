#!/usr/bin/env python

import sys
import os
import re
import argparse
import urllib.request
import shutil

class Example():
    def __init__(self, input, output):
        self.input = input
        self.output = output

class CompetitiveProgrammingSetup():

    def __init__(self, url, name, lang='cpp'):
        self.url = url
        self.name = name
        self.lang = 'cpp'
        self.examples = []

        if 'atcoder.jp' in self.url:
            self.type = 'atcoder'
        elif 'codeforces.com' in self.url:
            self.type = 'codeforces'
        elif 'u-aizu.ac.jp' in self.url:
            self.type = 'aoj'

    def run(self):
        self.__retrieve_examples()
        self.__write_examples_file()
        self.__create_template()

    def __retrieve_examples(self):
        request = urllib.request.Request(self.url)
        f = urllib.request.urlopen(request) 
        if(f.getcode() != 200):
            raise Exception("Page not found")
        content = f.read()
        content = content.decode(f.info().get_content_charset())

        if self.type == 'atcoder':
            self.__parse_atcoder_examples(content)
        elif self.type == 'codeforces':
            self.__parse_codeforces_examples(content)
        elif self.type == 'aoj':
            self.__parse_aoj_examples(content)

    def __parse_atcoder_examples(self, content):
        r = re.compile(r'Sample Input.*?<pre>(.*?)</pre>.*?Sample Output.*?<pre>(.*?)</pre>', re.MULTILINE|re.DOTALL)
        match_iter = r.finditer(content)
        for match in match_iter:
            if match.lastindex < 2:
                raise Exception("Failed to parse examples")
            example_input =  match.group(1).replace('\r\n', '\n')
            example_output =  match.group(2).replace('\r\n', '\n');
            self.examples.append(Example(example_input, example_output))

    def __parse_codeforces_examples(self, content):
        r = re.compile('<div class="input">.*?<pre>\n(.*?)</pre>.*?<div class="output">.*?<pre>\n(.*?)</pre>', re.MULTILINE|re.DOTALL)
        match_iter = r.finditer(content)
        for match in match_iter:
            if match.lastindex < 2:
                raise Exception("Failed to parse examples")
            example_input =  match.group(1).replace('\r\n', '\n')
            example_output =  match.group(2).replace('\r\n', '\n');
            self.examples.append(Example(example_input, example_output))

    def __parse_aoj_examples(self, content):
        r = re.compile('Sample Input.*?<pre>\n(.*?)</pre>.*?Sample Output.*?<pre>\n(.*?)</pre>', re.MULTILINE|re.DOTALL)
        match_iter = r.finditer(content)
        for match in match_iter:
            if match.lastindex < 2:
                raise Exception("Failed to parse examples")
            example_input =  match.group(1).replace('\r\n', '\n')
            example_output =  match.group(2).replace('\r\n', '\n');
            self.examples.append(Example(example_input, example_output))

    def __write_examples_file(self):
        file_path = self.name + '.txt'
        f = open(file_path, 'w')
        for example in self.examples:
            write_str = '''
<input>
%s</input>
<output>
%s</output>
''' % (example.input, example.output)
            f.write(write_str[1:])

    def __create_template(self):
        if self.lang == 'cpp':
            filename = self.name + '.cpp'
            shutil.copy('main.cpp', filename)

        elif self.lang == 'python':
            filename = self.name + '.py'
            shutil.copy('main.py', filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--name', '-n', required=True)
    parser.add_argument('--lang', '-l', default='cpp', required=False)
    ns = parser.parse_args()

    cpsetup = CompetitiveProgrammingSetup(ns.url, ns.name, ns.lang)
    cpsetup.run()
