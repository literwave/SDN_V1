from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QFormLayout, QLabel, \
    QHBoxLayout, QGridLayout, QMessageBox, QRadioButton, QVBoxLayout, QComboBox, QTextBrowser
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from ospfDialog import *
from inputdialog import inputDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from connection import *
import sys
import time
import json
import requests

# 忽略ssh警告连接
requests.packages.urllib3.disable_warnings()
# 构造头部信息
headers = {"Accept": "application/yang-data+json",
           "Content-type": "application/yang-data+json"
           }

api_url = "https://{}/restconf/data/ietf-interfaces:interfaces".format(devices[0])



class UI_form(QWidget):
    def __init__(self):
        super(UI_form, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.result = connection()
        self.method = 0
        self.command = 0
        self.device = 1
        self.resize(1130, 676)
        self.setWindowIcon(QIcon("./image/icon.jpg"))

        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(244, 244, 244))
        self.setPalette(palette)
        # self.setWindowFlags(Qt.FramelessWindowHint)  无边框

        self.btn1 = QPushButton("设备一")
        self.btn2 = QPushButton("设备二")
        self.btn3 = QPushButton("设备三")
        self.btn4 = QPushButton("设备四")

        self.radio1 = QRadioButton("方法一")
        self.radio2 = QRadioButton("方法二")
        self.radio3 = QRadioButton("方法三")

        self.label1 = QLabel("选用方法：")
        self.label2 = QLabel("请选择要执行的操作：")
        self.label3_1 = QLabel("设备一信息:")
        self.label3_2 = QLabel("设备二信息:")
        self.label3_3 = QLabel("设备三信息:")
        self.label3_4 = QLabel("设备四信息:")

        self.cb = QComboBox()
        self.cb.addItem('查看接口的摘要信息')
        self.cb.addItem('查看路由表')
        self.cb.addItem('显示所有的配置')
        self.cb.addItem('配置环回口')
        self.cb.addItem('配置OSPF')

        self.btext_1 = QTextBrowser()
        self.btext_2 = QTextBrowser()
        self.btext_3 = QTextBrowser()
        self.btext_4 = QTextBrowser()


        self.btn5 = QPushButton("确定")
        with open('QSS/btn.qss', 'r') as f:
            self.list_style = f.read()

        with open('QSS/widget.qss', 'r') as f:
            self.list_style_w = f.read()

        self.btn1.setStyleSheet(self.list_style)
        self.btn2.setStyleSheet(self.list_style)
        self.btn3.setStyleSheet(self.list_style)
        self.btn4.setStyleSheet(self.list_style)

        self.btn5.setStyleSheet(self.list_style)

        widget1 = QWidget()
        widget2 = QWidget()

        self.widget3_1 = QWidget()
        self.widget3_2 = QWidget()
        self.widget3_3 = QWidget()
        self.widget3_4 = QWidget()

        all_VBox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.label1)
        hbox.addWidget(self.radio1)
        hbox.addWidget(self.radio2)
        hbox.addWidget(self.radio3)

        Vbox = QVBoxLayout()
        Vbox.addWidget(self.label2)
        Vbox.addWidget(self.cb)
        Vbox.setSpacing(20)
        Vbox.setContentsMargins(0, 60, 0, 0)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.btn5)

        vbox2.setContentsMargins(0, 30, 0, 0)
        all_VBox.addLayout(hbox)
        # all_VBox.addStretch(1)
        all_VBox.addLayout(Vbox)
        all_VBox.addLayout(vbox2)
        all_VBox.addStretch(1)

        # all_VBox.setContentsMargins(0,15,0,0)
        widget2.setLayout(all_VBox)
        # widget2.setContentsMargins(0,0,0,0)
        # widget2.setLayout(Vbox)

        # 设置样式
        widget1.setStyleSheet(self.list_style_w)

        grid = QGridLayout()
        grid.addWidget(self.btn1, 0, 0)
        grid.addWidget(self.btn2, 1, 0)
        grid.addWidget(self.btn3, 2, 0)
        grid.addWidget(self.btn4, 3, 0)

        widget1.setLayout(grid)

        qvbox = QVBoxLayout()
        qvbox.addWidget(self.label3_1)
        qvbox.addWidget(self.btext_1)

        self.widget3_1.setLayout(qvbox)

        # self.widget3.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Window, QColor(0, 0, 0))
        # self.widget3.setPalette(palette)

        self.flay = QGridLayout()
        self.flay.addWidget(widget1, 0, 0, 1, 1)
        self.flay.addWidget(widget2, 0, 1, 1, 1)
        self.flay.addWidget(self.widget3_1, 0, 2, 1, 2)

        # qform=QFormLayout()
        # qform.addWidget(edit1)
        # qform.addWidget(edit2)
        # qform.addWidget(edit3)
        # qform.addWidget(btn1)

        self.command = "show ip interface brief"

        self.setLayout(self.flay)

        self.setWindowTitle("网络自动化客户端")

        self.btn2.clicked.connect(self.btn2_click)
        self.btn1.clicked.connect(self.click1)
        self.btn3.clicked.connect(self.btn3_click)
        self.btn4.clicked.connect(self.btn4_click)
        self.radio1.toggled.connect(self.radioStatus)
        self.radio2.toggled.connect(self.radioStatus)
        self.radio3.toggled.connect(self.radioStatus)
        self.cb.currentIndexChanged.connect(self.cbStatus)
        self.btn5.clicked.connect(self.method1)

    def click1(self):
        print(self.widget3_1.width())
        print(self.widget3_1.height())
        print("点我了")
        self.device = 1
        self.widget3_2.hide()
        self.widget3_3.hide()
        self.widget3_4.hide()
        self.widget3_1.show()

    def btn2_click(self):
        self.widget3_1.hide()
        self.widget3_3.hide()
        self.widget3_4.hide()
        qvbox = QVBoxLayout()
        qvbox.addWidget(self.label3_2)
        qvbox.addWidget(self.btext_2)
        self.widget3_2.setLayout(qvbox)
        self.flay.addWidget(self.widget3_2, 0, 2, 1, 2)
        self.setLayout(self.flay)
        self.widget3_2.show()
        self.device = 2

    def btn3_click(self):
        self.widget3_1.hide()
        self.widget3_2.hide()
        self.widget3_4.hide()
        qvbox = QVBoxLayout()
        qvbox.addWidget(self.label3_3)
        qvbox.addWidget(self.btext_3)
        self.widget3_3.setLayout(qvbox)
        self.flay.addWidget(self.widget3_3, 0, 2, 1, 2)
        self.setLayout(self.flay)
        self.widget3_3.show()
        self.device = 3

    def btn4_click(self):
        self.widget3_1.hide()
        self.widget3_2.hide()
        self.widget3_3.hide()
        qvbox = QVBoxLayout()
        qvbox.addWidget(self.label3_4)
        qvbox.addWidget(self.btext_4)
        self.widget3_4.setLayout(qvbox)
        self.flay.addWidget(self.widget3_4, 0, 2, 1, 2)
        self.setLayout(self.flay)
        self.widget3_4.show()
        self.device = 4

    def radioStatus(self):
        radioButton = self.sender()
        self.cb.clear()
        if radioButton.text() == '方法一':
            if radioButton.isChecked() == True:
                self.cb.addItem('查看接口的摘要信息')
                self.cb.addItem('查看路由表')
                self.cb.addItem('显示所有的配置')
                self.cb.addItem('配置环回口')
                self.cb.addItem('配置OSPF')
                self.method = '方法一'
        elif radioButton.text() == '方法二':
            if radioButton.isChecked() == True:
                self.cb.addItem("查看接口信息")
                self.cb.addItem("添加环回口")
                self.method = '方法二'
        else:
            if radioButton.isChecked() == True:
                self.cb.addItem("更改主机名")
                self.cb.addItem("添加环回")
                self.method = '方法三'

    def cbStatus(self, i):
        if self.cb.currentText() == '查看接口的摘要信息':
            self.command = "show ip interface brief"
        elif self.cb.currentText() == '查看路由表':
            self.command = "show ip route"
        elif self.cb.currentText() == '显示所有的配置':
            self.command = "show running-config"
        elif self.cb.currentText()=='配置环回口':
            self.command="add ip"
        elif self.cb.currentText()=='配置OSPF':
            self.command="OSPF"
        elif self.cb.currentText()=='查看接口信息':
            self.command="find"
            self.url=api_url
        elif self.cb.currentText()=='添加环回口':
            self.command="add"
            self.url=api_url+"/interface=Loopback99"
        elif self.cb.currentText() == '更改主机名':
            self.command="change"
        elif self.cb.currentText() == '添加环回':
            self.command="add_3"
        print(self.command)

    def method1(self):
        if self.method == 0:
            QMessageBox.about(self, '填写提示', '请选择方法')
        elif self.method == "方法一":
            if self.device == 1:
                if self.command == 'show ip interface brief':
                    output = self.result["sshcli"][0].send_command(self.command)
                    # self.btext_1.append(output)
                    # self.btext_1.moveCursor(self.btext_1.textCursor().End)
                    outputl = output.split()
                    # print(outputl)
                    count = int(len(outputl) / 6)

                    # print(count)
                    for i in range(1, count):
                        doutput = {"Interface": outputl[6 * i], "IP-Address": outputl[6 * i + 1],
                                   "OK?": outputl[6 * i + 2], "Method": outputl[6 * i + 3],
                                   "Status": outputl[6 * i + 4], "Protocol": outputl[6 * i + 5]}
                        str_te = json.dumps(doutput)
                        # print(type(str_te))
                        # print(str_te)
                        self.btext_1.append(str_te)
                        self.btext_1.moveCursor(self.btext_1.textCursor().End)
                elif self.command == 'show ip route':
                    output = self.result["sshcli"][0].send_command(self.command)
                    self.btext_1.append(output)
                    self.btext_1.moveCursor(self.btext_1.textCursor().End)

                elif self.command == 'show running-config':
                    output = self.result["sshcli"][0].send_command(self.command)
                    self.btext_1.append(output)
                    self.btext_1.moveCursor(self.btext_1.textCursor().End)

                elif self.command=='add ip':
                    self.input = inputDialog()
                    self.input.setWindowModality(Qt.ApplicationModal)

                    self.input._datasinal.connect(self.appdata)
                    self.input.exec()

                elif self.command=='OSPF':
                    self.ospf=ospfDialog()
                    self.ospf.setWindowModality(Qt.ApplicationModal)

                    self.ospf.lesignal.connect(self.appospf)
                    self.ospf.exec()



                    # name=self.input.name.text()
                    # ip=self.input.iplineEdit.text()
                    # net=self.input.netmask.text()
                    # des=self.input.deslineEdit.text()
                    # name="int loopback "+name
                    # ipnet="ip address "+ip+" "+net
                    # des="description "+des
                    # res=[]
                    # res.append(name)
                    # res.append(ipnet)
                    # res.append(des)
                    #
                    # print(res)
                    # output=self.result['sshcli'][0].send_config_set(res)
                    # self.btext_1.append(output)
                    # self.btext_1.moveCursor(self.btext_1.textCursor().End)






            elif self.device == 2:
                if self.command == 'show ip interface brief':
                    output = self.result["sshcli"][0].send_command(self.command)
                    outputl = output.split()
                    print(outputl)
                    count = int(len(outputl) / 6)

                    print(count)
                    for i in range(1, count):
                        doutput = {"Interface": outputl[6 * i], "IP-Address": outputl[6 * i + 1],
                                   "OK?": outputl[6 * i + 2], "Method": outputl[6 * i + 3],
                                   "Status": outputl[6 * i + 4], "Protocol": outputl[6 * i + 5]}
                        str_te = json.dumps(doutput)
                        print(type(str_te))
                        print(str_te)
                        self.btext_2.append(str_te)
                        self.btext_2.moveCursor(self.btext_2.textCursor().End)

                elif self.command == 'show ip route':
                    output = self.result["sshcli"][0].send_command(self.command)
                    self.btext_2.append(output)
                    self.btext_2.moveCursor(self.btext_2.textCursor().End)

                elif self.command == 'show running-config':
                    output = self.result["sshcli"][0].send_command(self.command)
                    self.btext_2.append(output)
                    self.btext_2.moveCursor(self.btext_2.textCursor().End)

                elif self.command=='add ip':
                    self.input = inputDialog()
                    self.input.setWindowModality(Qt.ApplicationModal)

                    self.input._datasinal.connect(self.appdata)
                    self.input.exec()

                elif self.command=='OSPF':
                    self.ospf=ospfDialog()
                    self.ospf.setWindowModality(Qt.ApplicationModal)

                    self.ospf.lesignal.connect(self.appospf)
                    self.ospf.exec()

            elif self.device == 3:
                if self.command == 'show ip interface brief':
                    output = self.result["sshcli"][0].send_command(self.command)
                    outputl = output.split()
                    print(outputl)
                    count = int(len(outputl) / 6)

                    print(count)
                    for i in range(1, count):
                        doutput = {"Interface": outputl[6 * i], "IP-Address": outputl[6 * i + 1],
                                   "OK?": outputl[6 * i + 2], "Method": outputl[6 * i + 3],
                                   "Status": outputl[6 * i + 4], "Protocol": outputl[6 * i + 5]}
                        str_te = json.dumps(doutput)
                        print(type(str_te))
                        print(str_te)
                        self.btext_3.append(str_te)
                        self.btext_3.moveCursor(self.btext_3.textCursor().End)

                elif self.command == 'show ip route':
                    output = self.result["sshcli"][0].send_command(self.command)
                    self.btext_3.append(output)
                    self.btext_3.moveCursor(self.btext_3.textCursor().End)

                elif self.command == 'show running-config':
                    output = self.result["sshcli"][0].send_command(self.command)
                    self.btext_3.append(output)
                    self.btext_3.moveCursor(self.btext_3.textCursor().End)

                elif self.command=='add ip':
                    self.input = inputDialog()
                    self.input.setWindowModality(Qt.ApplicationModal)

                    self.input._datasinal.connect(self.appdata)
                    self.input.exec()

                elif self.command=='OSPF':
                    self.ospf=ospfDialog()
                    self.ospf.setWindowModality(Qt.ApplicationModal)

                    self.ospf.lesignal.connect(self.appospf)
                    self.ospf.exec()

            elif self.device == 4:
                if self.command == 'show ip interface brief':
                    output = self.result["sshcli"][0].send_command(self.command)
                    outputl = output.split()
                    print(outputl)
                    count = int(len(outputl) / 6)

                    print(count)
                    for i in range(1, count):
                        doutput = {"Interface": outputl[6 * i], "IP-Address": outputl[6 * i + 1],
                                   "OK?": outputl[6 * i + 2], "Method": outputl[6 * i + 3],
                                   "Status": outputl[6 * i + 4], "Protocol": outputl[6 * i + 5]}
                        str_te = json.dumps(doutput)
                        print(type(str_te))
                        print(str_te)
                        self.btext_4.append(str_te)
                        self.btext_4.moveCursor(self.btext_4.textCursor().End)

                elif self.command == 'show ip route':
                    output = self.result["sshcli"][0].send_command(self.command)
                    self.btext_4.append(output)
                    self.btext_4.moveCursor(self.btext_4.textCursor().End)

                elif self.command == 'show running-config':
                    output = self.result["sshcli"][0].send_command(self.command)
                    self.btext_4.append(output)
                    self.btext_4.moveCursor(self.btext_4.textCursor().End)

                elif self.command=='add ip':
                    self.input = inputDialog()
                    self.input.setWindowModality(Qt.ApplicationModal)

                    self.input._datasinal.connect(self.appdata)
                    self.input.exec()

                elif self.command=='OSPF':
                    self.ospf=ospfDialog()
                    self.ospf.setWindowModality(Qt.ApplicationModal)

                    self.ospf.lesignal.connect(self.appospf)
                    self.ospf.exec()

        elif self.method=="方法二":
            if self.device==1:
                if self.command=="find":
                    resp = requests.get(self.url, auth=remoteInfo, headers=headers, verify=False)
                    res = resp.json()
                    t=json.dumps(res)
                    self.btext_1.append(t)
                    self.btext_1.moveCursor(self.btext_1.textCursor().End)
                elif self.command=="add":
                    yangConfig = {
                        "ietf-interfaces:interface": {
                            "name": "Loopback99",
                            "description": "WHATEVER99",
                            "type": "iana-if-type:softwareLoopback",
                            "enabled": True,
                            "ietf-ip:ipv4": {
                                "address": [
                                    {
                                        "ip": "99.99.99.99",
                                        "netmask": "255.255.255.0"
                                    }
                                ]
                            },
                            "ietf-ip:ipv6": {}
                        }
                    }



                    resp = requests.put(self.url, data=json.dumps(yangConfig), auth=remoteInfo, headers=headers, verify=False)

                    if (resp.status_code >= 200 and resp.status_code <= 299):
                        print("STATUS OK: {}".format(resp.status_code))
                        self.btext_1.append("添加成功")
                        self.btext_1.moveCursor(self.btext_1.textCursor().End)

                    else:
                        print("Error code {}, reply: {}".format(resp.status_code, resp.json()))
                        self.btext_1.append("添加失败")
                        self.btext_1.moveCursor(self.btext_1.textCursor().End)






            elif self.device==2:
                if self.command=="find":
                    resp = requests.get(self.url, auth=remoteInfo, headers=headers, verify=False)
                    res = resp.json()
                    t = json.dumps(res)
                    self.btext_2.append(t)
                    self.btext_2.moveCursor(self.btext_2.textCursor().End)

                elif self.command=="add":
                    yangConfig = {
                        "ietf-interfaces:interface": {
                            "name": "Loopback99",
                            "description": "WHATEVER99",
                            "type": "iana-if-type:softwareLoopback",
                            "enabled": True,
                            "ietf-ip:ipv4": {
                                "address": [
                                    {
                                        "ip": "99.99.99.99",
                                        "netmask": "255.255.255.0"
                                    }
                                ]
                            },
                            "ietf-ip:ipv6": {}
                        }
                    }



                    resp = requests.put(self.url, data=json.dumps(yangConfig), auth=remoteInfo, headers=headers, verify=False)

                    if (resp.status_code >= 200 and resp.status_code <= 299):
                        print("STATUS OK: {}".format(resp.status_code))
                        self.btext_2.append("添加成功")
                        self.btext_2.moveCursor(self.btext_2.textCursor().End)

                    else:
                        print("Error code {}, reply: {}".format(resp.status_code, resp.json()))
                        self.btext_2.append("添加失败")
                        self.btext_2.moveCursor(self.btext_2.textCursor().End)


            elif self.device==3:
                if self.command=="find":
                    resp = requests.get(self.url, auth=remoteInfo, headers=headers, verify=False)
                    res = resp.json()
                    t = json.dumps(res)
                    self.btext_3.append(t)
                    self.btext_3.moveCursor(self.btext_3.textCursor().End)
                elif self.command=="add":
                    yangConfig = {
                        "ietf-interfaces:interface": {
                            "name": "Loopback99",
                            "description": "WHATEVER99",
                            "type": "iana-if-type:softwareLoopback",
                            "enabled": True,
                            "ietf-ip:ipv4": {
                                "address": [
                                    {
                                        "ip": "99.99.99.99",
                                        "netmask": "255.255.255.0"
                                    }
                                ]
                            },
                            "ietf-ip:ipv6": {}
                        }
                    }



                    resp = requests.put(self.url, data=json.dumps(yangConfig), auth=remoteInfo, headers=headers, verify=False)

                    if (resp.status_code >= 200 and resp.status_code <= 299):
                        print("STATUS OK: {}".format(resp.status_code))
                        self.btext_3.append("添加成功")
                        self.btext_3.moveCursor(self.btext_3.textCursor().End)

                    else:
                        print("Error code {}, reply: {}".format(resp.status_code, resp.json()))
                        self.btext_3.append("添加失败")
                        self.btext_3.moveCursor(self.btext_3.textCursor().End)

            elif self.device==4:
                if self.command=="find":
                    resp = requests.get(self.url, auth=remoteInfo, headers=headers, verify=False)
                    res=resp.json()
                    t = json.dumps(res)
                    self.btext_4.append(t)
                    self.btext_4.moveCursor(self.btext_4.textCursor().End)

                elif self.command=="add":
                    yangConfig = {
                        "ietf-interfaces:interface": {
                            "name": "Loopback99",
                            "description": "WHATEVER99",
                            "type": "iana-if-type:softwareLoopback",
                            "enabled": True,
                            "ietf-ip:ipv4": {
                                "address": [
                                    {
                                        "ip": "99.99.99.99",
                                        "netmask": "255.255.255.0"
                                    }
                                ]
                            },
                            "ietf-ip:ipv6": {}
                        }
                    }



                    resp = requests.put(self.url, data=json.dumps(yangConfig), auth=remoteInfo, headers=headers, verify=False)

                    if (resp.status_code >= 200 and resp.status_code <= 299):
                        print("STATUS OK: {}".format(resp.status_code))
                        self.btext_4.append("添加成功")
                        self.btext_4.moveCursor(self.btext_4.textCursor().End)

                    else:
                        print("Error code {}, reply: {}".format(resp.status_code, resp.json()))
                        self.btext_4.append("添加失败")
                        self.btext_4.moveCursor(self.btext_4.textCursor().End)


        elif self.method =="方法三":
            if self.device==1:
                if self.command=="change":
                    print("no")
                    netconf_data = """
                    <config><native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                        <hostname>csr2kv</hostname>
                    </native></config>"""

                    self.result["manager"][0].edit_config(target="running", config=netconf_data)
                    self.btext_1.append("修改主机名成功")
                    self.btext_1.moveCursor(self.btext_1.textCursor().End)

                elif self.command=="add_3":
                    print("why")
                    netconf_data = """
                    <config>
                     <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                      <interface>
                       <Loopback>
                        <name>111</name>
                        <description>TEST111</description>
                        <ip>
                         <address>
                          <primary>
                           <address>100.100.100.100</address>
                           <mask>255.255.255.0</mask>
                          </primary>
                         </address>
                        </ip>
                       </Loopback>
                      </interface>
                     </native>
                    </config>
                    """

                    self.result["manager"][0].edit_config(target="running", config=netconf_data)
                    print("this")
                    self.btext_1.append("添加环口成功")
                    self.btext_1.moveCursor(self.btext_1.textCursor().End)

            elif self.device==2:
                if self.command == "change":
                    netconf_data = """
                                    <config><native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                                        <hostname>csr2kv</hostname>
                                    </native></config>"""

                    self.result["manager"][0].edit_config(target="running", config=netconf_data)
                    self.btext_2.append("修改主机名成功")
                    self.btext_2.moveCursor(self.btext_2.textCursor().End)

                elif self.command == "add_3":

                    netconf_data = """
                    <config>
                     <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                      <interface>
                       <Loopback>
                        <name>111</name>
                        <description>TEST111</description>
                        <ip>
                         <address>
                          <primary>
                           <address>100.100.100.100</address>
                           <mask>255.255.255.0</mask>
                          </primary>
                         </address>
                        </ip>
                       </Loopback>
                      </interface>
                     </native>
                    </config>
                    """

                    self.result["manager"][0].edit_config(target="running", config=netconf_data)
                    self.btext_2.append("添加环口成功")
                    self.btext_2.moveCursor(self.btext_2.textCursor().End)

            elif self.device==3:
                if self.command=="change":
                    netconf_data = """
                                    <config><native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                                        <hostname>csr2kv</hostname>
                                    </native></config>"""

                    self.result["manager"][0].edit_config(target="running", config=netconf_data)
                    self.btext_3.append("修改主机名成功")
                    self.btext_3.moveCursor(self.btext_3.textCursor().End)

                elif self.command == "add_3":
                    netconf_data = """
                    <config>
                     <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                      <interface>
                       <Loopback>
                        <name>111</name>
                        <description>TEST111</description>
                        <ip>
                         <address>
                          <primary>
                           <address>100.100.100.100</address>
                           <mask>255.255.255.0</mask>
                          </primary>
                         </address>
                        </ip>
                       </Loopback>
                      </interface>
                     </native>
                    </config>
                    """

                    self.result["manager"][0].edit_config(target="running", config=netconf_data)
                    self.btext_3.append("添加环口成功")
                    self.btext_3.moveCursor(self.btext_3.textCursor().End)

            elif self.device==4:
                if self.command=="change":
                    netconf_data = """
                                    <config><native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                                        <hostname>csr2kv</hostname>
                                    </native></config>"""

                    self.result["manager"][0].edit_config(target="running", config=netconf_data)
                    self.btext_4.append("修改主机名成功")
                    self.btext_4.moveCursor(self.btext_4.textCursor().End)

                elif self.command == "add_3":
                    netconf_data = """
                    <config>
                     <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                      <interface>
                       <Loopback>
                        <name>111</name>
                        <description>TEST111</description>
                        <ip>
                         <address>
                          <primary>
                           <address>100.100.100.100</address>
                           <mask>255.255.255.0</mask>
                          </primary>
                         </address>
                        </ip>
                       </Loopback>
                      </interface>
                     </native>
                    </config>
                    """

                    self.result["manager"][0].edit_config(target="running", config=netconf_data)
                    self.btext_4.append("添加环口成功")
                    self.btext_4.moveCursor(self.btext_4.textCursor().End)



    def appdata(self,name,ip,net,des):
        name = "int loopback " + name
        ipnet = "ip address " + ip + " " + net
        des = "description " + des
        res = []
        res.append(name)
        res.append(ipnet)
        res.append(des)

        print(res)
        output = self.result['sshcli'][0].send_config_set(res)
        if self.device==1 and self.method=="方法一":

            self.btext_1.append(output)
            self.btext_1.moveCursor(self.btext_1.textCursor().End)

        elif self.device==2 and self.method=="方法一":

            self.btext_2.append(output)
            self.btext_2.moveCursor(self.btext_2.textCursor().End)

        elif self.device==3 and self.method=="方法一":
            self.btext_3.append(output)
            self.btext_3.moveCursor(self.btext_3.textCursor().End)

        elif self.device==4 and self.method=="方法一":
            self.btext_4.append(output)
            self.btext_4.moveCursor(self.btext_4.textCursor().End)

        self.input.close()
        self.input.destroy()


    def appospf(self,process,Id,IP,netmask):
        process="router ospf "+process
        id="router-id "+Id
        IP="network "+IP+" "+netmask+" area 0"
        res=[]
        res.append(process)
        res.append(id)
        res.append(IP)
        print(res)
        output = self.result['sshcli'][0].send_config_set(res)
        if self.device == 1 and self.method == "方法一":

            self.btext_1.append(output)
            self.btext_1.moveCursor(self.btext_1.textCursor().End)

        elif self.device == 2 and self.method == "方法一":

            self.btext_2.append(output)
            self.btext_2.moveCursor(self.btext_2.textCursor().End)

        elif self.device == 3 and self.method == "方法一":
            self.btext_3.append(output)
            self.btext_3.moveCursor(self.btext_3.textCursor().End)

        elif self.device == 4 and self.method == "方法一":
            self.btext_4.append(output)
            self.btext_4.moveCursor(self.btext_4.textCursor().End)

        self.ospf.close()
        self.ospf.destroy()






        # print(self.method)
        # self.command=self.cb.currentText()
        # print(type(self.command))
        # print(self.cb.currentText())
        # print(self.result)
        # output=self.result["sshcli"][0].send_command(self.command)
        # print(output)
        # self.btext.append(output)
        # self.btext.moveCursor(self.btext.textCursor().End)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI_form()
    ui.show()
    time.sleep(2)
    QMessageBox.about(ui, '连接提示', '有四台设备已连接上')

    sys.exit(app.exec_())
