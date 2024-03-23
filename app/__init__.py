import os
import sys

try:
    os.chdir(sys.path[0])
    print("更改工作目录成功", sys.path[0])
except FileNotFoundError:
    print("更改工作目录失败")
