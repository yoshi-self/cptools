#!/usr/bin/env python

import sys
import re
import subprocess
import argparse

class CompetitiveProgrammingTest():

    def __init__(self, source, test=None, limit=2):
        self.source = source

        m = re.match(r'^([^\.]*?)\.(.*?)$', source)
        self.name = m.group(1)
        ext = m.group(2)
        if ext == 'cpp':
            self.lang = 'cpp'
        elif ext == 'py':
            self.lang = 'python3'

        if test is not None:
            self.test = test
        else:
            self.test = self.name + '.txt'

        self.timeout = limit
        self.inputs = []
        self.outputs = []

    def run(self, build=False):
        self.build = build
        self.__parse_test()

        if self.lang == 'cpp':
            if self.build:
                ret = self.__build_cpp()
                if ret != 0:
                    print('build failed')
                    sys.exit(1)
                else:
                    print('buil succeeded')
            self.__run_cpp()
        elif self.lang == 'python3':
            self.__run_python3()

    def __parse_test(self):
        f = open(self.test)
        test_content = f.read()
        flags = (re.MULTILINE | re.DOTALL)
        r = re.compile(r'<input>\n(.*?)</input>\n<output>\n(.*?)</output>', flags);
        m_iter = r.finditer(test_content)
        for m in m_iter:
            self.inputs.append(m.group(1))
            self.outputs.append(m.group(2))

    def __build_cpp(self):
        print('##### Build %s #####' % (self.source))

        build_command = ['g++', '-xc++', '-std=c++14', '-lm', '-DLOCAL', '-Wall', '-Wextra']
        run_command = build_command + [self.source] + ['-o', self.name]
        p = subprocess.run(run_command, stdout=subprocess.PIPE)
        build_output = p.stdout
        return p.returncode

    def __run_with_test(self, run_command):
        for i in range(len(self.inputs)):
            print('\n##### Test %d #####' % (i + 1))
            test_input = self.inputs[i]
            print('-- input --\n%s' % (test_input), end='')
            print('-----------')
            test_answer = self.outputs[i]

            p = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf_8')
            try:
                test_output = p.communicate(test_input, timeout=self.timeout)[0] # read stdout
            except subprocess.TimeoutExpired as e:
                test_output = p.stdout.read(256)
                p.kill()
                test_output += '\nTime limit exceeded: %d sec\n' % self.timeout
 
            if test_output == test_answer:
                print('\n[Correct answer]')
            else:
                print('\n[Wrong answer]')
                print('-- your output --\n%s' % test_output, end='')
                print('-- expected output --\n%s' % (test_answer), end='')
            #i += 1

    def __run_cpp(self):
        run_command = ['./' + self.name]
        self.__run_with_test(run_command)

    def __run_python3(self):
        i = 0
        run_command = ['python', self.source]
        self.__run_with_test(run_command)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('--test', '-t', default=None, required=False)
    parser.add_argument('--build', '-b', action='store_true')
    parser.add_argument('--limit', '-l', type=int, default=2, required=False)
    ns = parser.parse_args()

    cptest = CompetitiveProgrammingTest(ns.source, ns.test, ns.limit)

    cptest.run(ns.build)
