#!/usr/bin/env python
# coding=UTF-8
'''
Author: user
Date: 2021-10-10 20:58:03
LastEditors: user
LastEditTime: 2021-10-11 11:47:44
Descripttion: 
'''
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# import QSqlTableModel

from Ui_new_student import Ui_Dialog
import Ui_new_student
# from new_student import my_student


class my_student(QDialog, Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        Ui_new_student.Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.model = QSqlQueryModel()
        self.connect_database()
        self.create_table()
        self.query_table()

        self.insert_button.clicked.connect(self.on_insert_button)
        self.delete_button.clicked.connect(self.on_delete_button)
        self.alter_button.clicked.connect(self.on_alter_button)
        self.sort_button.clicked.connect(self.on_sort_button)
        self.search_button.clicked.connect(self.on_search_button)
        self.return_button.clicked.connect(self.query_table)

    def connect_database(self):
        # self.database=
        self.database = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName("student_list.db")
        if self.database.open():
            print("创建或打开数据库成功")
        else:
            print("创建或打开数据库失败")

    def create_table(self):
        self.query = QSqlQuery()
        table_content = "create table my_student_python(" + "id INT PRIMARY KEY NOT NULL," + "name TEXT NOT NULL," + "sex TEXT NOT NULL," + "age INT NOT NULL," + "score REAL)"
        if self.query.exec(table_content):
            print("创建或打开表格成功")
        else:
            print("创建或打开表格失败")

    def close_database(self):
        self.database.close()

    def query_table(self):
        self.query = QSqlQuery()
        query_content = "select * from my_student_python"
        # self.model = QSqlQueryModel()
        self.model.setQuery(query_content)
        self.tableView.setModel(self.model)

    def on_insert_button(self):
        # self.connect_database()
        # self.create_table()
        self.query = QSqlQuery()
        print('as')
        id = self.id_edit.text()
        name = self.name_edit.text()
        sex = self.sex_edit.text()
        score = self.score_edit.text()
        age = self.age_edit.text()
        print(id, name, sex, score, age)
        query_content = "insert into my_student_python values({},'{}','{}',{},{})".format(
            id, name, sex, age, score)
        if self.query.exec(query_content):
            print("插入数据成功")
            self.query_table()
        else:
            print("插入数据失败")
        # self.close_database()

    def on_delete_button(self):
        # self.connect_database()
        # self.create_table()
        self.query = QSqlQuery()
        id = self.id_edit.text()
        query_content = "delete from my_student_python where id={}".format(
            id)
        # self.model = QSqlQueryModel()
        if self.query.exec(query_content):
            print("删除数据成功")
            self.query_table()
        else:
            print("删除数据失败")
        # self.close_database()

    def on_alter_button(self):
        # self.connect_database()
        # self.create_table()
        self.query = QSqlQuery()
        
        id = self.id_edit.text()
        name = self.name_edit.text()
        sex = self.sex_edit.text()
        score = self.score_edit.text()
        age = self.age_edit.text()
        query_content = "update my_student_python set id={},name='{}',sex='{}',age={},score={} where id={}".format(
            id, name, sex, age, score, id)
        if self.query.exec(query_content):
            print("修改数据成功")
            self.query_table()
        else:
            print("修改数据失败")
        # self.close_database()

    def on_sort_button(self):
        # self.connect_database()
        # self.create_table()
        self.query = QSqlQuery()
        value = self.id_combox.currentText()
        if self.way_combox.currentIndex() == 0:
            way = "ASC"
        else:
            way = "DESC"
        query_content = "select * from my_student_python order by {} {}".format(
            value, way)
        if self.query.exec(query_content):
            print("整理数据成功")
            self.model.setQuery(query_content)
            self.tableView.setModel(self.model)
        else:
            print("排序失败")
        # self.close_database()

    def on_search_button(self):
        # self.connect_database()
        # self.create_table()
        self.query = QSqlQuery()
        id = self.id_edit.text()
        query_content = "select * from my_student_python where id={}".format(
            id)
        # self.model = QSqlQueryModel()
        if self.query.exec(query_content):
            print("寻找数据成功")
            self.model.setQuery(query_content)
            self.tableView.setModel(self.model)
        else:
            print("寻找数据失败")
        # self.close_database()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # MainWindow = QDialog()
    # ui = Ui_new_student.Ui_Dialog()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    a = my_student()
    a.show()
    sys.exit(app.exec_())
