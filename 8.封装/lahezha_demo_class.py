#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-04-12 19:15:34
LastEditors: user
LastEditTime: 2022-04-12 20:19:17
Descripttion: 
'''
#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-04-12 18:54:41
LastEditors: user
LastEditTime: 2022-04-12 19:13:05
Descripttion: 
'''
import lahezha as lhz 
import pandas as pd



class try_lahezha():
    def __init__(self, inputfile):
      self.inputfile = inputfile
           
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
        
    def class_show_yichang(self):
        self.my_lof()
        df=lhz.show_yichang(self.after_lof_data)
        print(df)
        return df

if __name__ == "__main__":
    inputfile = "D:\\1_kaoyan\college_ending\\400仪表数据--全\middata - 副本\拉合闸最终.csv"
    demo=try_lahezha(inputfile=inputfile)
    demo.show_yuanshitu()
    demo.class_show_yichang()
    