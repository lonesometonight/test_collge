#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-02-15 17:03:28
LastEditors: user
LastEditTime: 2022-02-20 23:09:13
Descripttion: 
'''
import pandas as pd
inputfile=""
data = pd.read_csv(inputfile,sep='\t',encoding='utf-8')
data=data.drop(columns="Unnamed: 0",axis=1)
data['regionId']=data['regionId'].astype('object')
data_change=data.T