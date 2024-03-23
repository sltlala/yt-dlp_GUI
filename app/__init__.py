import os

try:
    os.chdir(os.path.dirname(__file__))
    print("更改工作目录成功", os.path.dirname(__file__))
except FileNotFoundError:
    print("更改工作目录失败")
