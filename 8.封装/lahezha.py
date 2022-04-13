#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-04-12 18:20:10
LastEditors: user
LastEditTime: 2022-04-12 20:54:07
Descripttion: 
'''
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
import matplotlib
#设置字体为楷体
matplotlib.rcParams['font.sans-serif'] = ['KaiTi']

###########################################
# 这两个函数是下面data_chuli_lahezha函数要用的
def time_JiSuan(data):
    new_0c1o = data['new_0c1o']
    relayStatus_0c1o = data['relayStatus_0c1o']
    new_meterNo = data['new_meterNo']
    meterNo = data['meterNo']
    next_relayUpdateTime = data['next_relayUpdateTime']
    new_relayUpdateTime = data['new_relayUpdateTime']
    if meterNo == new_meterNo and new_0c1o == 0 and relayStatus_0c1o == 1:
        if_time = next_relayUpdateTime-new_relayUpdateTime
    else:
        if_time = 0
    return if_time


def shijianchuo(data):
    new_0c1o = data['new_0c1o']
    relayStatus_0c1o = data['relayStatus_0c1o']
    new_meterNo = data['new_meterNo']
    meterNo = data['meterNo']
    next_relayUpdateTime = data['next_relayUpdateTime']
    new_relayUpdateTime = data['new_relayUpdateTime']
    new_relayUpdateTime = int(datetime.timestamp(new_relayUpdateTime))
    next_relayUpdateTime = int(datetime.timestamp(next_relayUpdateTime))
    if meterNo == new_meterNo and new_0c1o == 0 and relayStatus_0c1o == 1:
        if_time = next_relayUpdateTime-new_relayUpdateTime
    else:
        if_time = 0
    return if_time

############################################

# 该函数输入pd.read_csv后的数据
    # <class 'pandas.core.frame.DataFrame'>
    # RangeIndex: 24641 entries, 0 to 24640
    # Data columns (total 3 columns):
    #  #   Column            Non-Null Count  Dtype 
    # ---  ------            --------------  ----- 
    #  0   meterNo           24641 non-null  int64 
    #  1   relayStatus_0c1o  24641 non-null  int64 
    #  2   relayUpdateTime   24641 non-null  object
    # dtypes: int64(2), object(1)
    # memory usage: 577.6+ KB

# 处理后得到data_fina 是dataframe
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 400 entries, 0 to 399
    # Data columns (total 4 columns):
    #  #   Column        Non-Null Count  Dtype  
    # ---  ------        --------------  -----  
    #  0   new_meterNo   400 non-null    int64  
    #  1   lhz_cishu     400 non-null    float64
    #  2   If_Time_chuo  400 non-null    int64  
    #  3   mean_min      400 non-null    float64
    # dtypes: float64(2), int64(2)
    # memory usage: 15.6 KB

def data_chuli_lahezha(data_YuanLai):
    data_time = data_YuanLai.copy(deep=1)  # 进行复制，使得后面操作不影响前面
    # 2.1、调整数据类型，并且复制新的列
    data_time['new_relayUpdateTime'] = data_time['relayUpdateTime'].apply(pd.to_datetime)
    data_time['relayStatus_0c1o'] = data_time['relayStatus_0c1o'].fillna(1).astype('int64')
    data_time['new_meterNo'] = data_time['meterNo'].shift(-1).fillna('10023160000352').astype('int64')
    data_time['new_0c1o'] = data_time['relayStatus_0c1o'].shift(-1).fillna(1).astype('int64')
    data_time['next_relayUpdateTime'] = data_time['new_relayUpdateTime'].shift(-1).fillna('2017-05-01 17:00:00').apply(pd.to_datetime)
    # print("2、增加新的序列成功\n")

    # 3、计算时间戳
    data_time_JiSuan = data_time.copy(deep=1)
    data_time_JiSuan['NoIf_time'] = data_time_JiSuan['next_relayUpdateTime'] - data_time_JiSuan['new_relayUpdateTime']
    data_time_JiSuan['If_Time'] = data_time_JiSuan.apply(time_JiSuan, axis=1)
    data_time_JiSuan['If_Time_chuo'] = data_time_JiSuan.apply(shijianchuo, axis=1)
    # print("3、计算时间戳\n")

    # 4、开始聚合
    # 4.1、计算所有时间
    data_group = data_time_JiSuan.copy(deep=1)
    datagroup_shijianchuo = data_group.groupby('new_meterNo', as_index=0).agg({'If_Time_chuo': 'sum'})
    # 4.2、计算次数
    data_cishu = data_time_JiSuan.copy(deep=1)
    data_cishu = data_cishu[(data_cishu['relayStatus_0c1o'] == 1)].groupby(['meterNo'])['relayStatus_0c1o'].sum()#这里是序列
    # 4.3、把序列转换成dataframe
    data_lhz_cishu = {'new_meterNo': data_cishu.index,
                    'lhz_cishu': data_cishu.values}
    data_lhz_cishu = pd.DataFrame(data_lhz_cishu)
    # print("4、开始聚合\n")

    # 5、开始合并次数和时间
    data_fina = data_lhz_cishu.merge(datagroup_shijianchuo, how='inner', on='new_meterNo')
    # print("5、开始合并次数和时间\n")

    # 6、开始绘图
    data_fina['mean_min'] = (data_fina['If_Time_chuo']/data_fina['lhz_cishu'])/60 #转换成为分钟
    # #! 6.1、进行标准化
    
    data_fina['mean_min_yuanshi']=data_fina.mean_min
    data_fina['lhz_cishu_yuanshi']=data_fina.lhz_cishu  
    
    data_fina['mean_min']=data_fina.mean_min.apply(lambda x : (x-np.min(data_fina.mean_min))/(np.max(data_fina.mean_min) - np.min(data_fina.mean_min)))
    data_fina['lhz_cishu']=data_fina.lhz_cishu.apply(lambda x : (x-np.min(data_fina.lhz_cishu))/(np.max(data_fina.lhz_cishu) - np.min(data_fina.lhz_cishu)))
    return data_fina

def draw_lahezha(data_fina):
    plt.title("次数和平均值")
    plt.scatter(data_fina['lhz_cishu'], data_fina['mean_min'],
                color='k', s=3, label='Data points')
    plt.show()

####################################################

# 输入
    # <class 'pandas.core.frame.DataFrame'>
    # Int64Index: 400 entries, 0 to 399
    # Data columns (total 4 columns):
    #  #   Column        Non-Null Count  Dtype  
    # ---  ------        --------------  -----  
    #  0   new_meterNo   400 non-null    int64  
    #  1   lhz_cishu     400 non-null    float64
    #  2   If_Time_chuo  400 non-null    int64  
    #  3   mean_min      400 non-null    float64
    # dtypes: float64(2), int64(2)
    # memory usage: 15.6 KB

# 输出
    # <class 'pandas.core.frame.DataFrame'>
    # RangeIndex: 400 entries, 0 to 399
    # Data columns (total 6 columns):
    #  #   Column   Non-Null Count  Dtype  
    # ---  ------   --------------  -----  
    #  0   meterNo  400 non-null    object 
    #  1   times    400 non-null    float64
    #  2   all_s    400 non-null    float64
    #  3   aver     400 non-null    float64
    #  4   score    400 non-null    float64
    #  5   z_score  400 non-null    float64
    # dtypes: float64(5), object(1)
    # memory usage: 18.9+ KB

   
def suanfa_Lof(data_fina,k=100,value_yichang=0.05):
    # 7、lof算法引进
    # 7.1、处理输入
    lof_data = data_fina.copy(deep=1)
    Y = lof_data.values #转换为数组
    Y1 = Y[:, 1]
    Y2 = Y[:, 3]
    Y_pic = np.c_[Y1, Y2]
    # 7.2、机器学习部分
    clf = LocalOutlierFactor(n_neighbors=k, contamination=value_yichang)

    # 有两个 第一个是他的xy两个轴的度量相差太大 所以在计算密度的时候他的次数看起来权重很小，第二个就是他的k值不能设置的太小 不然可能他的可达距离也就是k过于局部，特别是对过于密集的点

    y_pred = clf.fit_predict(Y_pic)
    X_scores = clf.negative_outlier_factor_
    # 7.3、把分数加入序列
    Y_all = np.c_[Y, X_scores]
    last_data = pd.DataFrame(Y_all)#变成dataframe
    # 7.4、转变数据类型，添加列名
    after_lof_data = last_data.copy(deep=1)
    after_lof_data.columns = ['meterNo', 'times', 'all_s', 'aver', 'aver_shiji','times_shiji','score']
    after_lof_data['meterNo'] = after_lof_data['meterNo'].astype('int64').astype('object')
    after_lof_data['times'] = after_lof_data['times'].astype('float64')
    # 7.5、把分数转成绝对值，并且添加成新的一列
    after_lof_data['z_score'] = after_lof_data['score'].abs()
    # print("7、lof算法引进\n")
    return after_lof_data

def draw_lof_lahezha(after_lof_data,value_yichang=380):
    # 8、排序
    sort_after_lof_data = after_lof_data.copy(deep=1)
    sort_after_lof_data.sort_values("z_score", inplace=True)
    # print("8、排序\n")

    # 9、处理相关值并且绘图
    # sort_after_lof_data.iloc[380, 5]
    # 9.1、分类
    sort_after_lof_data.loc[sort_after_lof_data['z_score']>= sort_after_lof_data.iloc[value_yichang, 5], 'class'] = 0
    sort_after_lof_data.loc[sort_after_lof_data['z_score'] < sort_after_lof_data.iloc[value_yichang, 5], 'class'] = 1
    # 9.2、绘图
    plt.title("LOF")
    plt.scatter(sort_after_lof_data['times'][:value_yichang],sort_after_lof_data['aver'][:value_yichang], color='r', label="inliner")
    plt.scatter(sort_after_lof_data['times'][value_yichang:],sort_after_lof_data['aver'][value_yichang:], color='g', label="outliner")
    plt.legend()
    plt.show()
    # print("9、处理相关值并且绘图\n")
    
def show_yichang(after_lof_data,value_yichang=380):
        # 8、排序
    sort_after_lof_data = after_lof_data.copy(deep=1)
    sort_after_lof_data.sort_values("z_score", inplace=True)
    # print("8、排序\n")
    return sort_after_lof_data[value_yichang:]