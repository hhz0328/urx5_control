# urx5_control
使用python，对UR5机器人进行控制，实现了自定义工作空间下的自定义步长扫描

##使用的package
1.python-urx
链接：https://github.com/SintefManufacturing/python-urx
2.numpy
3.tqdm

##遇到的Bug
（1）pip install urx，由于pip维护问题，导致urx版本过低。导致movel函数，使用异常，发生报错
解决方法：直接到
