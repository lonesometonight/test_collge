#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-04-12 18:54:41
LastEditors: user
LastEditTime: 2022-04-12 19:17:01
Descripttion: 
'''
import lahezha as lhz 
import pandas as pd

inputfile = "D:\\1_kaoyan\college_ending\\400仪表数据--全\middata - 副本\拉合闸最终.csv"

def try_lahezha():
    # 1、读数据
    data_YuanLai = pd.read_csv(inputfile, encoding='utf-8')
    # 2、开始处理数据
    data_fina=lhz.data_chuli_lahezha(data_YuanLai)
    # 3、画出原始图
    lhz.draw_lahezha(data_fina)
    # 4、算法LOF引进
    after_lof_data=lhz.suanfa_Lof(data_fina)
    # 5、画出lof图像
    lhz.draw_lof_lahezha(after_lof_data)
    # lhz.show_yichang(after_lof_data)

if __name__ == "__main__":
    try_lahezha()
    