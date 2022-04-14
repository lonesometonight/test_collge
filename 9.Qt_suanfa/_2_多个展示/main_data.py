#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-04-13 23:02:01
LastEditors: user
LastEditTime: 2022-04-14 16:28:14
Descripttion: 
'''
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Ui_tu_jiemian import Ui_Dialog
import Ui_tu_jiemian

import lahezha as lhz 
import pandas as pd
import buPingHengDu as bphd



class my_lhz(QDialog, Ui_Dialog):
    def __init__(self,inputfile):
        QDialog.__init__(self)
        Ui_tu_jiemian.Ui_Dialog.__init__(self)
        self.setupUi(self)
        
        self.inputfile = inputfile 
        
        self.button_yuantu.clicked.connect(self.show_yuanshitu)
        self.button_loftu.clicked.connect(self.show_lof_image)
        
        self.button_biaoming.clicked.connect(self.show_data_chuli_bph)
        
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
        lhz.draw_lof_lahezha(self.after_lof_data)
        # lhz.show_yichang(after_lof_data)
        
    ####################################
    # 不平衡度，相关函数
    def show_data_chuli_bph(self):
        get_biaoming=self.lineEdit_biaoming.text()
        bphd.plot_bphd(biao_name=get_biaoming)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    inputfile = "D:\\1_kaoyan\college_ending\\400仪表数据--全\middata - 副本\拉合闸最终.csv"
    a = my_lhz(inputfile)
    a.show()
    sys.exit(app.exec_())