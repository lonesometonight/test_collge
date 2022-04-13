#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-03-27 16:59:12
LastEditors: user
LastEditTime: 2022-03-28 16:14:44
Descripttion: 
'''

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import Ui_jie_mian
from Ui_jie_mian import Ui_Dialog
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("Qt5Agg")


# 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键
class Figure_Canvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)
        # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure

        FigureCanvas.__init__(self, fig)  # 初始化父类
        self.setParent(parent)
        # self.setParent

        # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        self.axes = fig.add_subplot(111)

    def test(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y = [23, 21, 32, 13, 3, 132, 13, 3, 1]
        self.axes.plot(x, y)


class Mytest(QDialog, Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        Ui_jie_mian.Ui_Dialog.__init__(self)
        self.setupUi(self)
        # # 设置窗口标题
        # self.setWindowTitle('My First App')
        # self.setFixedSize(800, 600)

        # # ===通过graphicsView来显示图形
        # self.graphicsView = QtWidgets.QGraphicsView()  # 第一步，创建一个QGraphicsView
        # self.graphicsView.setObjectName("graphicsView")

        dr = Figure_Canvas()
        # 实例化一个FigureCanvas
        dr.test()  # 画图
        # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicsView控件中，必须先放到graphicScene，然后再把graphicscene放到graphicsView中
        graphicscene = QtWidgets.QGraphicsScene()
        # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        graphicscene.addWidget(dr)
        # 第五步，把QGraphicsScene放入QGraphicsView
        self.graphicsView.setScene(graphicscene)
        self.graphicsView.show()  # 最后，调用show方法呈现图形！Voila!!
        # self.setCentralWidget(self.graphicsView)
        # self.graphicsView.setFixedSize(800, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mytest = Mytest()

    mytest.show()
    app.exec_()
