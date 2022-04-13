#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-04-12 19:43:15
LastEditors: user
LastEditTime: 2022-04-12 20:02:29
Descripttion: 
'''
class my_demo():
    def __init__(self, name):
      self.name = name
      self.age = 17
      
    def age_mingnian(self):
        self.m_age = self.age  + 1
        return self.m_age
    
    def age_hounian(self):
        self.age_mingnian()
        h_age = self.m_age+1
        return h_age
    
if __name__ == "__main__":
    demo = my_demo('lili')
    # m_age=demo.age_mingnian()
    # print('m_age',m_age)
    h_age=demo.age_hounian()
    print('h_age',h_age)