# urx5_control
使用python，对UR5机器人进行控制，实现了自定义工作空间下的自定义步长扫描

## 使用的package
1.python-urx

链接：https://github.com/SintefManufacturing/python-urx

2.numpy

3.tqdm

## 遇到的Bug
（1）pip install urx，由于pip维护问题，导致urx版本过低。导致movel函数，使用异常，发生报错。

解决方法：使用pip uninstall卸载原先的urx。直接到github下载最新版python-urx的zip源码，放到工作空间下。

（2）math3d版本过高，不再依赖numpy库，导致传参时，发生异常。

解决办法：降版本，卸载4.0版本，使用3*低版本，即可解决报错。
