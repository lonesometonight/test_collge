#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-04-13 22:52:02
LastEditors: user
LastEditTime: 2022-04-14 16:29:19
Descripttion: 
'''
#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-04-12 20:59:35
LastEditors: user
LastEditTime: 2022-04-13 11:28:14
Descripttion: 
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# #################################################################
# 输入相一相二相三的电压文件地址
# 输出 [错误，异常，正常]


def data_chuli_bph(data1, data2, data3):
    wrong_biao = []
    yichang_biao = []
    zhengchang_biao = []
    # 1.2、把数据变成dataframe的形式
    pd1 = pd.read_csv(data1, encoding='utf-8')
    pd2 = pd.read_csv(data2, encoding='utf-8')
    pd3 = pd.read_csv(data3, encoding='utf-8')
    # 1.3、判断三个表的字段是否一样
    # 经检测，三张表的列名一致，所以只需要将任意一个表的列名提取出来即可
    biao1 = pd1.columns
    biaotou = list(biao1)
    # 转变成为列表，注意除了第一个'MeterNo'外，其余的后面都有一个空格'10023160000011 '
    for i in list(range(len(biaotou)))[1:]:

        #! 2、分离数据，把每一个仪器表单独提取出来
        str1 = pd1[['meterNo', biaotou[i]]].copy(deep=1)
        str2 = pd2[['meterNo', biaotou[i]]].copy(deep=1)
        str3 = pd3[['meterNo', biaotou[i]]].copy(deep=1)

        # 2.1、把三相表和并在一起
        diyige = pd.concat([str1, str2, str3], axis=1)
        # 2.2、重新定义列名
        diyige.columns = ['MeterNo', biaotou[i]+'1',
                          'MeterNo1', biaotou[i]+'2',
                          'MeterNo2', biaotou[i]+'3']
        # 2.3、把仪表名字，相1，相2，相3提出来
        diyige_right = diyige[['MeterNo', biaotou[i] +
                               '1', biaotou[i]+'2', biaotou[i]+'3']]

        # 2.4、填补空缺值
        diyige_right = diyige_right.fillna(0.0)
        # print("2、分离数据成功\n")

        #! 3、计算0的占比
        # 3.1、当占比超过80%，输出数据一场
        num_0 = diyige_right[biaotou[i] +
                             '1'][diyige_right[biaotou[i]+'1'] == 0].count()
        num_all = diyige_right[biaotou[i]+'1'].count()
        bili_0 = num_0/num_all

        if bili_0 >= 0.8:
            print(biaotou[i]+"data error\n")
            # num_yichang=num_yichang+1
            wrong_biao.append(int(biaotou[i]))
            continue

        # print("3、计算0的占比成功\n")

        #! 4、计算不平衡度
        diyige_right['Mean_123'] = 1/3 * \
            (diyige_right.iloc[:, 1] +
             diyige_right.iloc[:, 2]+diyige_right.iloc[:, 3])

        diyige_right['fen_zi'] = abs((diyige_right.iloc[:, 1]-diyige_right['Mean_123']))+abs(
            (diyige_right.iloc[:, 2]-diyige_right['Mean_123']))+abs((diyige_right.iloc[:, 3]-diyige_right['Mean_123']))
        diyige_right['fen_mu'] = 3*diyige_right['Mean_123']
        diyige_right['不平衡度'] = diyige_right['fen_zi'] / \
            (diyige_right['fen_mu']+0.001)

        # print("4、计算不平衡度成功\n")

        # #! 5、开始画图
        # diyige_right['MeterNo']=diyige_right['MeterNo'].apply(pd.to_datetime)
        # plt.scatter(diyige_right['MeterNo'],diyige_right['不平衡度'],color="g", s=3,label='不平衡度')
        # plt.show()
        # print("5、开始画图成功\n")

        #! 6、计算指标
        aver = diyige_right['不平衡度'].mean()
        jicha = diyige_right['不平衡度'].max()-diyige_right['不平衡度'].min()
        four_point = diyige_right['不平衡度'].quantile(0.75)

        if aver <= 0.2 and four_point <= 0.2:
            zhengchang_biao.append(int(biaotou[i]))
        else:
            yichang_biao.append(int(biaotou[i]))

        print(biaotou[i], aver, jicha)
        # print("6、计算指标成功\n")

    return [wrong_biao, yichang_biao, zhengchang_biao]
#######################################################################

#######################################################################
# 输入相一相二相三的电压文件地址和表名
# 输出 图表
# 返回 [biao_name,diyige_right['MeterNo'],diyige_right['不平衡度']]
# 表名，时间数据，不平衡度


def plot_bphd(biao_name,data1="D:\\1_kaoyan\college_ending\\400仪表数据--全\middata - 副本\仪器分时数据——按照不同类型类型来区分(单相,三相)\\1_有数据\处理后\核心数据\FourHundred_loadprofile_three_P8311三相表相1的平均电压.csv", data2="D:\\1_kaoyan\college_ending\\400仪表数据--全\middata - 副本\仪器分时数据——按照不同类型类型来区分(单相,三相)\\1_有数据\处理后\核心数据\FourHundred_loadprofile_three_P8312三相表相2的平均电压.csv", data3="D:\\1_kaoyan\college_ending\\400仪表数据--全\middata - 副本\仪器分时数据——按照不同类型类型来区分(单相,三相)\\1_有数据\处理后\核心数据\FourHundred_loadprofile_three_P8313三相表相3的平均电压.csv"):

    biao_name = biao_name + ' '
    # 1.2、把数据变成dataframe的形式
    pd1 = pd.read_csv(data1, encoding='utf-8')
    pd2 = pd.read_csv(data2, encoding='utf-8')
    pd3 = pd.read_csv(data3, encoding='utf-8')
    #! 2、分离数据，把每一个仪器表单独提取出来
    str1 = pd1[['meterNo', biao_name]].copy(deep=1)
    str2 = pd2[['meterNo', biao_name]].copy(deep=1)
    str3 = pd3[['meterNo', biao_name]].copy(deep=1)

    # 2.1、把三相表和并在一起
    diyige = pd.concat([str1, str2, str3], axis=1)
    # 2.2、重新定义列名
    diyige.columns = ['MeterNo', biao_name+'1',
                      'MeterNo1', biao_name+'2',
                      'MeterNo2', biao_name+'3']
    # 2.3、把仪表名字，相1，相2，相3提出来
    diyige_right = diyige[['MeterNo', biao_name +
                           '1', biao_name+'2', biao_name+'3']]

    # 2.4、填补空缺值
    diyige_right = diyige_right.fillna(0.0)
    # print("2、分离数据成功\n")

    # print("3、计算0的占比成功\n")

    #! 4、计算不平衡度
    diyige_right['Mean_123'] = 1/3 * \
        (diyige_right.iloc[:, 1] +
         diyige_right.iloc[:, 2]+diyige_right.iloc[:, 3])

    diyige_right['fen_zi'] = abs((diyige_right.iloc[:, 1]-diyige_right['Mean_123']))+abs(
        (diyige_right.iloc[:, 2]-diyige_right['Mean_123']))+abs((diyige_right.iloc[:, 3]-diyige_right['Mean_123']))
    diyige_right['fen_mu'] = 3*diyige_right['Mean_123']
    diyige_right['不平衡度'] = diyige_right['fen_zi'] / \
        (diyige_right['fen_mu']+0.001)

    # print("4、计算不平衡度成功\n")

    #! 5、开始画图
    diyige_right['MeterNo'] = diyige_right['MeterNo'].apply(pd.to_datetime)
    plt.scatter(diyige_right['MeterNo'],
                diyige_right['不平衡度'], color="g", s=3, label='不平衡度')
    plt.title(str(int(biao_name))+'时间-不平衡度图', fontsize=13)
    plt.ylabel('不平衡度', fontsize=15)
    plt.xlabel('时间', fontsize=15)
    plt.legend()
    plt.show()
    # print("5、开始画图成功\n")
    return [str(int(biao_name)), diyige_right['MeterNo'], diyige_right['不平衡度']]

######################################################################
