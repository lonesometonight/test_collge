#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-04-09 13:15:02
LastEditors: user
LastEditTime: 2022-04-09 21:31:21
Descripttion: 
'''
# 可见，正常用户的电流不平衡度几乎为零，且波动范围极小;而窃电用户电流不平衡度明显较高，最高值达到了0.4左右。
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#! 1、导入数据

# 1.1、定义列表的名字，data1、2、3就是相1、2、3
data1 = "D:\\1_kaoyan\college_ending\\400仪表数据--全\middata - 副本\仪器分时数据——按照不同类型类型来区分(单相,三相)\\1_有数据\处理后\核心数据\FourHundred_loadprofile_three_P8391三相表相1的平均电流.csv"
data2 = "D:\\1_kaoyan\college_ending\\400仪表数据--全\middata - 副本\仪器分时数据——按照不同类型类型来区分(单相,三相)\\1_有数据\处理后\核心数据\FourHundred_loadprofile_three_P8392三相表相2的平均电流.csv"
data3 = "D:\\1_kaoyan\college_ending\\400仪表数据--全\middata - 副本\仪器分时数据——按照不同类型类型来区分(单相,三相)\\1_有数据\处理后\核心数据\FourHundred_loadprofile_three_P8393三相表相3的平均电流.csv"

num_yichang = 0
wrong_biao=[]
yichang_biao=[]
zhengchang_biao=[]

# 1.2、把数据变成dataframe的形式
pd1 = pd.read_csv(data1,encoding='utf-8')
pd2=pd.read_csv(data2,encoding='utf-8')
pd3=pd.read_csv(data2,encoding='utf-8')

# 1.3、判断三个表的字段是否一样
# 经检测，三张表的列名一致，所以只需要将任意一个表的列名提取出来即可
biao1=pd1.columns
biaotou=list(biao1)
#转变成为列表，注意除了第一个'MeterNo'外，其余的后面都有一个空格'10023160000011 '

print("1、导入数据成功\n")
for i in list(range(len(biaotou)))[1:]:
    
    #! 2、分离数据，把每一个仪器表单独提取出来
    str1=pd1[[biaotou[0],biaotou[i]]].copy(deep=1)
    str2=pd2[[biaotou[0],biaotou[i]]].copy(deep=1)
    str3=pd3[[biaotou[0],biaotou[i]]].copy(deep=1)

    # 2.1、把三相表和并在一起
    diyige=pd.concat([str1,str2,str3],axis=1)
    # 2.2、重新定义列名
    diyige.columns = ['MeterNo',biaotou[i]+'1',
                    'MeterNo1',biaotou[i]+'2',
                    'MeterNo2',biaotou[i]+'3']
    # 2.3、把仪表名字，相1，相2，相3提出来
    diyige_right=diyige[['MeterNo',biaotou[i]+'1',biaotou[i]+'2',biaotou[i]+'3']]

    # 2.4、填补空缺值
    diyige_right=diyige_right.fillna(0.0)
    print("2、分离数据成功\n")

    #! 3、计算0的占比
    # 3.1、当占比超过80%，输出数据一场
    num_0=diyige_right[biaotou[i]+'1'][diyige_right[biaotou[i]+'1']==0].count()
    num_all=diyige_right[biaotou[i]+'1'].count()
    bili_0=num_0/num_all
    
    if bili_0 >=0.8:
        print(biaotou[i]+"data error\n")
        num_yichang=num_yichang+1
        wrong_biao.append(biaotou[i])
        continue
    
    print("3、计算0的占比成功\n")



    #! 4、计算不平衡度
    diyige_right['Mean_123']=1/3*(diyige_right.iloc[:,1]+diyige_right.iloc[:,2]+diyige_right.iloc[:,3])
    
    diyige_right['fen_zi']=abs((diyige_right.iloc[:,1]-diyige_right['Mean_123']))+abs((diyige_right.iloc[:,2]-diyige_right['Mean_123']))+abs((diyige_right.iloc[:,3]-diyige_right['Mean_123']))
    diyige_right['fen_mu']=3*diyige_right['Mean_123']
    diyige_right['不平衡度']=diyige_right['fen_zi']/(diyige_right['fen_mu']+0.001)

    print("4、计算不平衡度成功\n")

    # #! 5、开始画图
    # diyige_right['MeterNo']=diyige_right['MeterNo'].apply(pd.to_datetime)
    # plt.scatter(diyige_right['MeterNo'],diyige_right['不平衡度'],color="g", s=3,label='不平衡度')
    # plt.show()
    # print("5、开始画图成功\n")

    #! 6、计算指标
    aver=diyige_right['不平衡度'].mean()
    jicha = diyige_right['不平衡度'].max()-diyige_right['不平衡度'].min()
    
    if aver <= 0.2 and jicha<=0.2:
        zhengchang_biao.append(biaotou[i])
    else:
        yichang_biao.append(biaotou[i])
    
    print(biaotou[i],aver,jicha)
    print("6、计算指标成功\n")
  
print('一共有多少个数据表'+str(len(biaotou))+'\n')
print('一共有多少个错误数据'+str(num_yichang)+'\n')  
print(wrong_biao)
print('一共有多少正常数据'+str(len(zhengchang_biao))+'\n')
print(zhengchang_biao)
print('一共有多少异常数据'+str(len(yichang_biao))+'\n')
print(yichang_biao)
print('错误数据占比'+str(num_yichang/len(biaotou))+'\n')
print('异常数据占比'+str(len(yichang_biao)/len(biaotou))+'\n')
print('正常数据占比'+str(len(zhengchang_biao)/len(biaotou))+'\n')