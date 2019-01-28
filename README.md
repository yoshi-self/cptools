# cptools
Setup and test scripts for competitive programming

## Usage
### Setup
```
# ./cpsetup problem_url -n name [-l language]
./cpsetup https://atcoder.jp/contests/abc100/tasks/abc100_a -n ABC100A
```
This will parse examples and copy main.cpp to current directory.
* ABC100A.cpp: a copy of main.cpp
* ABC100A.txt: example inputs and outputs for test script

### Test
```
# ./cptest name [-t testfile] [-b]
./cptest ABC110A -b
```
Test ABC100A.cpp if inputs and outputs match.
-t: test file name (ABC100A.txt is used if not specified)
-b: build source before run
