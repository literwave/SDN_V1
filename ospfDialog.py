#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020-07-31 11:46
# @Author : Curry
# @Site : https://github.com/coolbreeze2
# @File : ospfDialog.py
# @Software: PyCharm


from PyQt5.QtWidgets import QGridLayout, QDialog, QApplication, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QFont,QIcon
import sys


class ospfDialog(QDialog):
    lesignal = pyqtSignal(str,str,str,str)

    def __init__(self):
        super(ospfDialog, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(QIcon("./image/icon.jpg"))
        self.setWindowTitle("设置OSPF")
        self.resize(503,354)

        with open('QSS/btn.qss', 'r') as f:
            self.list_style_b = f.read()

        with open('QSS/lineEdit.qss', 'r') as f:
            self.list_style_l = f.read()

        font = QFont()
        font.setFamily('Microsoft YaHei')
        font.setPixelSize(25)


        label1 = QLabel("Process number:")
        label2 = QLabel("Router-Id:")
        label3 = QLabel("IP:")
        label4 = QLabel("Netmask:")

        label1.setFont(font)
        label2.setFont(font)
        label3.setFont(font)
        label4.setFont(font)

        self.line1 = QLineEdit()
        self.line2 = QLineEdit()
        self.line3 = QLineEdit()
        self.line4 = QLineEdit()

        btn1=QPushButton("确定")
        btn2=QPushButton("关闭")


        btn1.setStyleSheet(self.list_style_b)
        btn2.setStyleSheet(self.list_style_b)

        self.line1.setStyleSheet(self.list_style_l)
        self.line2.setStyleSheet(self.list_style_l)
        self.line3.setStyleSheet(self.list_style_l)
        self.line4.setStyleSheet(self.list_style_l)

        self.line2.setInputMask('000.000.000.000;_')
        self.line3.setInputMask('000.000.000.000;_')
        self.line4.setInputMask('000.000.000.000;_')




        glay=QGridLayout()
        glay.addWidget(label1,0,0,1,1)
        glay.addWidget(self.line1,0,1,1,1)
        glay.addWidget(label2, 1, 0, 1, 1)
        glay.addWidget(self.line2, 1, 1, 1, 1)
        glay.addWidget(label3, 2, 0, 1, 1)
        glay.addWidget(self.line3, 2, 1, 1, 1)
        glay.addWidget(label4, 3, 0, 1, 1)
        glay.addWidget(self.line4, 3, 1, 1, 1)
        glay.addWidget(btn1, 5, 0, 1, 1)
        glay.addWidget(btn2, 5, 1, 1, 1)

        self.setLayout(glay)

        btn2.clicked.connect(self.close)
        btn1.clicked.connect(self.send_data)

    def send_data(self):
        data1=self.line1.text()
        data2=self.line2.text()
        data3 = self.line3.text()
        data4 = self.line4.text()
        print(data1)

        self.lesignal.emit(data1,data2,data3,data4)
        print(data1)
        print(data2)
        print(data3)
        print(data4)

        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    dia = ospfDialog()
    dia.show()
    sys.exit(app.exec_())
