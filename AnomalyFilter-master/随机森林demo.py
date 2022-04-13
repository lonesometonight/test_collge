#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2022-02-26 21:48:13
LastEditors: user
LastEditTime: 2022-02-27 14:59:23
Descripttion: 
'''
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
 
rng = np.random.RandomState(42)
 
# 生成训练数据
X = 0.3 * rng.randn(100, 2)
X_train = np.r_[X + 2, X - 2]
# 产生一些常规的新观察
X = 0.3 * rng.randn(20, 2)
X_test = np.r_[X + 2, X - 2]
# 产生一些异常新奇的观察结果
X_outliers = rng.uniform(low=-4, high=4, size=(20, 2))
 
# fit the model
clf = IsolationForest(max_samples=100,
                      random_state=rng, contamination='auto')
clf.fit(X_train)
y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)
y_pred_outliers = clf.predict(X_outliers)
 
# 画出直线，样本，和离平面最近的矢量
xx, yy = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
 

plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)
plt.title("IsolationForest")
 
b1 = plt.scatter(X_train[:, 0], X_train[:, 1], c='white',
                 s=20, edgecolor='k')
b2 = plt.scatter(X_test[:, 0], X_test[:, 1], c='green',
                 s=20, edgecolor='k')
c = plt.scatter(X_outliers[:, 0], X_outliers[:, 1], c='red',
                s=20, edgecolor='k')
plt.axis('tight')
plt.xlim((-5, 5))
plt.ylim((-5, 5))
plt.legend([b1, b2, c],
           ["training observations",
            "new regular observations", "new abnormal observations"],
           loc="upper left")
plt.show()