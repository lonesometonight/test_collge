#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-04-13 12:06:52
LastEditors: user
LastEditTime: 2022-04-13 19:06:37
Descripttion: 
'''
import pandas as pd
import numpy as np
import plotly.express as px 
from sklearn.ensemble import IsolationForest

def data_chuli_yongdianliang(filename_day):
    # 1、读原始数据
    data_day_yuanlai = pd.read_csv(filename_day,encoding='utf-8')
    data_day_yuanlai['MeterNo']=data_day_yuanlai['MeterNo'].apply(pd.to_datetime)
    data_day_yuanlai['month'] = data_day_yuanlai.MeterNo.dt.month
    
    # <class 'pandas.core.frame.DataFrame'>
    # RangeIndex: 366 entries, 0 to 365
    # Columns: 402 entries, MeterNo to month
    # dtypes: datetime64[ns](1), float64(399), int64(2)
    # memory usage: 1.1 MB
    
    # 2、进行数据透视
    data_day_toushibiao = data_day_yuanlai.copy(deep=1)
    data_day_toushibiao=data_day_toushibiao.fillna(0)
    toushibiao_values=list(data_day_yuanlai.columns)[1:-1]
    month_sum_toushibiao = pd.pivot_table(data_day_toushibiao,index='month',values=toushibiao_values,aggfunc=np.sum)
    
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 12 entries, 1 to 12
    # Columns: 400 entries, 10014164400011  to 10023160000352 
    # dtypes: float64(399), int64(1)
    # memory usage: 37.6 KB
    
    # 3、计算涨幅
    zd_month_sum_toushibiao = month_sum_toushibiao.copy(deep=1)
    zhangdie=zd_month_sum_toushibiao['10014164400011 ']
    zhangdie=zhangdie.reset_index()
    zhangdie['next_status']=zhangdie['10014164400011 '].shift(-1).fillna(zhangdie['10014164400011 '][11])
    zhangdie['ZhangDie']=(zhangdie['next_status']-zhangdie['10014164400011 '])/zhangdie['next_status']
    
    # <class 'pandas.core.frame.DataFrame'>
    # RangeIndex: 12 entries, 0 to 11
    # Data columns (total 4 columns):
    # #   Column           Non-Null Count  Dtype  
    # ---  ------           --------------  -----  
    # 0   month            12 non-null     int64  
    # 1   10014164400011   12 non-null     float64
    # 2   next_status      12 non-null     float64
    # 3   ZhangDie         12 non-null     float64
    # dtypes: float64(3), int64(1)
    # memory usage: 512.0 bytes
    
    # 4、循环找异常
    xunhuan_data = month_sum_toushibiao.copy(deep=1)
    all_list = xunhuan_data.columns
    yichang_list=[]
    for i in range(len(all_list)):
        zhangdie_xunhuan = xunhuan_data[all_list[i]]
        zhangdie_xunhuan=zhangdie_xunhuan.reset_index()
        zhangdie_xunhuan['next_status']=zhangdie_xunhuan[all_list[i]].shift(-1).fillna(zhangdie_xunhuan[all_list[i]][11])
        zhangdie_xunhuan['ZhangDie']=(zhangdie_xunhuan['next_status']-zhangdie_xunhuan[all_list[i]])/zhangdie_xunhuan['next_status']
        month_count = 0
        for j in list(zhangdie_xunhuan.ZhangDie):
            month_count = month_count+1
            if j >= 0.2 and j != 1:
                yichang_list.append([all_list[i],month_count,j])
                break
    data_yichang = pd.DataFrame(yichang_list)   
    data_yichang.columns = ['MeterNo','yichang_month','zhangdie']  
    
    # <class 'pandas.core.frame.DataFrame'>
    # RangeIndex: 48 entries, 0 to 47
    # Data columns (total 3 columns):
    # #   Column         Non-Null Count  Dtype  
    # ---  ------         --------------  -----  
    # 0   MeterNo        48 non-null     object 
    # 1   yichang_month  48 non-null     int64  
    # 2   zhangdie       48 non-null     float64
    # dtypes: float64(1), int64(1), object(1)
    # memory usage: 1.2+ KB
       
    return [data_yichang,month_sum_toushibiao]


def find_yichang_month(data_yichang):
    yichang_toushibiao1 = pd.pivot_table(data_yichang,index=['MeterNo'],values=['yichang_month','zhangdie'],aggfunc=np.mean)
    yichang_month=pd.DataFrame(yichang_toushibiao1.yichang_month.value_counts())
    yichang_month=yichang_month.reset_index()
    yichang_month.columns=['month','freq']
    return yichang_month

def zhunBei_GuLiSenLin(month_sum_toushibiao):
    data_dianliang = month_sum_toushibiao.copy(deep=1)
    # 判断每个月非0的个数
    num_not0 = []
    for col in list(data_dianliang.columns):
        zero = len(data_dianliang[data_dianliang[col] != 0])
        num_not0.append([col,zero])
        data_not0 = pd.DataFrame(num_not0)
    data_not0.columns=['meterNo','num_not0']
    # 计算总的用电量
    data_all_dianliang = data_dianliang.copy(deep=1)
    sum_all=data_all_dianliang.sum(axis=0)
    data_all_dianliang = pd.DataFrame(sum_all)
    data_all_dianliang=data_all_dianliang.reset_index()
    data_all_dianliang.columns=['meterNo','sum_all']
    data_all_dianliang['sum_all'] = data_all_dianliang['sum_all'].astype('int64')
    # 合并两张表
    data_fina = data_not0.merge(data_all_dianliang, how='inner', on='meterNo')
    data_fina['aver_month']=data_fina['sum_all']/(data_fina['num_not0']+0.01)
    data_fina['aver_month']=data_fina['aver_month'].astype('int64')
    data_fina['std_month']=list(data_dianliang.std()[:])
    data_fina['std_month']=data_fina['std_month'].astype('int64')
    
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 400 entries, 0 to 399
    # Data columns (total 5 columns):
    # #   Column      Non-Null Count  Dtype 
    # ---  ------      --------------  ----- 
    # 0   meterNo     400 non-null    object
    # 1   num_not0    400 non-null    int64 
    # 2   sum_all     400 non-null    int64 
    # 3   aver_month  400 non-null    int64 
    # 4   std_month   400 non-null    int64 
    # dtypes: int64(4), object(1)
    # memory usage: 18.8+ KB
    
    return data_fina

def suanfa_GuLiSenLin(data_fina,num_features=4,yichang_rate=0.05):
    data_guli=data_fina.copy(deep=1)
    data_guli=data_guli.set_index('meterNo')
    data_guli_values = data_guli.copy(deep=1)
    iforest = IsolationForest(n_estimators=100, max_samples='auto',  
                          contamination=yichang_rate, max_features=num_features,  
                          bootstrap=False, n_jobs=-1, random_state=1)
    #  fit_predict 函数 训练和预测一起 可以得到模型是否异常的判断，-1为异常，1为正常
    data_guli['label'] = iforest.fit_predict(data_guli_values) 
    # 预测 decision_function 可以得出 异常评分
    data_guli['scores'] = iforest.decision_function(data_guli_values)
    
    # <class 'pandas.core.frame.DataFrame'>
    # Index: 400 entries, 10014164400011  to 10023160000352 
    # Data columns (total 7 columns):
    # #   Column      Non-Null Count  Dtype  
    # ---  ------      --------------  -----  
    # 0   num_not0    400 non-null    int64  
    # 1   sum_all     400 non-null    int64  
    # 2   aver_month  400 non-null    int64  
    # 3   std_month   400 non-null    int64  
    # 4   label       400 non-null    int32  
    # 5   scores      400 non-null    float64
    # 6   anomaly     400 non-null    object 
    # dtypes: float64(1), int32(1), int64(4), object(1)
    # memory usage: 23.4+ KB
    
    return data_guli

def draw_gulisenlin_zhifangtu(data_guli):
    data_guli['anomaly'] = data_guli['label'].apply(lambda x: 'outlier' if x==-1  else 'inlier') 
    fig = px.histogram(data_guli,x='scores',color='anomaly') 
    fig.show()
    
def draw_gulisenlin_sanDianTu(data_guli):
    data_guli['anomaly'] = data_guli['label'].apply(lambda x: 'outlier' if x==-1  else 'inlier') 
    fig = px.scatter_3d(data_guli,x='num_not0', 
                       y='sum_all', 
                       z='aver_month', 
                       color='anomaly') 
    fig.show()