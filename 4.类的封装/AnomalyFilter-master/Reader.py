# -*- coding:utf-8 -*-
# Author: lishiyun19 
# Mail: lishiyun19@163.com
# Created Time: Tue Sep 19 14:20:55 2017

import csv


def read():
    with open(r'D:\1_kaoyan\college_ending\college_ending_code\AnomalyFilter-master\HEC.csv', 'rt') as file:
        reader = csv.DictReader(file)
        thpDict = [thp for thp in reader]

    with open(r'D:\1_kaoyan\college_ending\college_ending_code\AnomalyFilter-master\CPU.csv', 'rt') as file:
        reader = csv.DictReader(file)
        cpuDict = [cpu for cpu in reader]
    return thpDict,cpuDict
