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

（3）调试过程中，使用movel函数时，机械臂的运行速度和加速度，不要太大。否则会触发机械臂的保护，自动抱死。

解决办法：设置 a = 0.1, v = 0.2这个参数比较好

（4）如果机械臂末端加装了夹爪或者重物，切记要添加tcp末端质量的参数。

解决办法：1）使用上位机，直接在人机交互界面添加； 2）使用urx的内置函数set_tcp和set_payload；

## 总结&展望
第一个python项目，希望自己写程序时，摆脱for循环，多用库，规范自己的代码格式。有一说一，pycharm一键规范书写格式的功能真好用，哈哈哈。————2023.10.25
