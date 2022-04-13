#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-03-28 16:57:26
LastEditors: user
LastEditTime: 2022-04-04 21:47:54
Descripttion: 
'''
# 1、先把matplotlib嵌入pyqt5
# 1.1、通过matplotlib.backends.backend_qt5agg类连接Pyqt5
from Ui_jie_mian import Ui_Dialog
import Ui_jie_mian
import numpy as np
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
# 2、pyqt的相关的模块导入
# from PyQt5.QtWidgets import QApplication, QDialog


# 2.1、连接图形文件

# 3、创建一个matplotlib图形绘制类

class My_figure(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        # 3.1、创建第一个figure
        self.fig = Figure(figsize=(width, height), dpi=100)
        # 3.2、在父类里面激活Figure窗口
        super(My_figure, self).__init__(self.fig)
        # 此句必不可少，否则不能显示图形
        # 3.3、创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)

    # 4、就是画图，【可以在此类中画，也可以在其它类中画】
    # def plotsin(self):
    #     self.axes0 = self.fig.add_subplot(111)
    #     t = np.arange(0.0, 3.0, 0.01)
    #     s = np.sin(2 * np.pi * t)
    #     self.axes0.plot(t, s)
    # def plotcos(self):
    #     t = np.arange(0.0, 3.0, 0.01)
    #     s = np.sin(2 * np.pi * t)
    #     self.axes.plot(t, s)


class My_test(QDialog, Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        Ui_jie_mian.Ui_Dialog.__init__(self)
        self.setupUi(self)
        # 第五步：定义MyFigure类的一个实例
        self.F = My_figure(width=3, height=2, dpi=100)
        self.plotcos()
        self.gridlayout = QGridLayout(self.groupBox)
        # 继承容器groupBox
        self.gridlayout.addWidget(self.F, 0, 1)

        # 新增
        self.F1 = My_figure(width=5, height=4, dpi=100)
        self.plotother()
        self.gridlayout1 = QGridLayout(self.groupBox_2)
        self.gridlayout1.addWidget(self.F1, 2, 2)

    def plotcos(self):
        t = np.arange(0.0, 5.0, 0.01)
        s = np.cos(2 * np.pi * t)
        self.F.axes.plot(t, s)
        self.F.fig.suptitle("cos")

    def plotother(self):
        # F1 = My_figure(width=5, height=4, dpi=100)
        self.F1.fig.suptitle("Figuer_4")
        self.F1.axes1 = self.F1.fig.add_subplot(221)
        x = np.arange(0, 50)
        y = np.random.rand(50)
        self.F1.axes1.hist(y, bins=50)
        self.F1.axes1.plot(x, y)
        self.F1.axes1.bar(x, y)
        self.F1.axes1.set_title("hist")
        self.F1.axes2 = self.F1.fig.add_subplot(222)
        # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y = [23, 21, 32, 13, 3, 132, 13, 3, 1]
        self.F1.axes2.plot(x, y)
        self.F1.axes2.set_title("line")
        # 散点图
        self.F1.axes3 = self.F1.fig.add_subplot(223)
        self.F1.axes3.scatter(np.random.rand(20), np.random.rand(20))
        self.F1.axes3.set_title("scatter")
        # 折线图
        self.F1.axes4 = self.F1.fig.add_subplot(224)
        x = np.arange(0, 5, 0.1)
        self.F1.axes4.plot(x, np.sin(x), x, np.cos(x))
        self.F1.axes4.set_title("sincos")
        # self.gridlayout.addWidget(F1, 0, 2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = My_test()
    main.show()
    # app.installEventFilter(main)
    sys.exit(app.exec_())
