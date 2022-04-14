#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-04-13 20:48:59
LastEditors: user
LastEditTime: 2022-04-13 21:17:16
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

# 导入关于拉合闸的库
import lahezha as lhz 
import pandas as pd

class My_figure(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        # 3.1、创建第一个figure
        self.fig = Figure(figsize=(width, height), dpi=100)
        # 3.2、在父类里面激活Figure窗口
        super(My_figure, self).__init__(self.fig)
        # 此句必不可少，否则不能显示图形
        # 3.3、创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)

        
class My_lhz(QDialog, Ui_Dialog):
    def __init__(self,inputfile):
        QDialog.__init__(self)
        Ui_jie_mian.Ui_Dialog.__init__(self)
        self.setupUi(self)
        
        
        # 1、定义MyFigure类的一个实例
        self.inputfile = inputfile
        self.F = My_figure(width=3, height=2, dpi=100)
        self.show_lof_image()
        self.gridlayout = QGridLayout(self.groupBox)
        # 继承容器groupBox
        self.gridlayout.addWidget(self.F, 0, 1)
        
    def data_chuli(self):
        # 1、读数据
        data_YuanLai = pd.read_csv(self.inputfile, encoding='utf-8')
        # 2、开始处理数据
        self.data_fina=lhz.data_chuli_lahezha(data_YuanLai)
    
    def show_yuanshitu(self):    
        # 3、画出原始图
        self.data_chuli()
        lhz.draw_lahezha(self.data_fina)
        
    def my_lof(self):
        self.data_chuli()   
        # 4、算法LOF引进
        self.after_lof_data=lhz.suanfa_Lof(self.data_fina)
        
    def show_lof_image(self):
        self.my_lof()
        # 5、画出lof图像
        data_yichangzhi=lhz.draw_lof_lahezha(self.after_lof_data)
        
        self.F.fig.suptitle("LOF")
        self.F.axes.scatter(data_yichangzhi[0]['times'][:data_yichangzhi[1]],data_yichangzhi[0]['aver'][:data_yichangzhi[1]], color='r', label="inliner")
        self.F.axes.scatter(data_yichangzhi[0]['times'][data_yichangzhi[1]:],data_yichangzhi[0]['aver'][data_yichangzhi[1]:], color='g', label="outliner")
        self.F.fig.legend()
        # plt.show()
 
        
    def class_show_yichang(self):
        self.my_lof()
        df=lhz.show_yichang(self.after_lof_data)
        print(df)
        return df

if __name__ == "__main__":
    app = QApplication(sys.argv)
    inputfile = "D:\\1_kaoyan\college_ending\\400仪表数据--全\middata - 副本\拉合闸最终.csv"
    main = My_lhz(inputfile=inputfile)
    main.show()
    # app.installEventFilter(main)
    sys.exit(app.exec_())