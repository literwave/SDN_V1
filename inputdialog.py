from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QApplication, QWidget, QPushButton, QLabel, QGridLayout,QDialogButtonBox
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import Qt,pyqtSignal
import sys


class inputDialog(QDialog):
    _datasinal=pyqtSignal(str,str,str,str)
    def __init__(self):
        super(inputDialog, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("配置环回口")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(QIcon("./image/icon.jpg"))
        # self.flag=0
        gridLayout = QGridLayout()

        self.name = QLineEdit()
        self.iplineEdit = QLineEdit()
        self.netmask = QLineEdit()
        self.deslineEdit = QLineEdit()
        font=QFont()
        font.setFamily('Microsoft YaHei')
        font.setPixelSize(25)
        self.setFixedSize(417,452)


        btn1 = QPushButton("确定")
        btn2 = QPushButton("关闭")

        with open('QSS/btn.qss', 'r') as f:
            self.list_style_b = f.read()

        with open('QSS/lineEdit.qss', 'r') as f:
            self.list_style_l = f.read()

        self.name.setStyleSheet(self.list_style_l)
        self.iplineEdit.setStyleSheet(self.list_style_l)
        self.netmask.setStyleSheet(self.list_style_l)
        self.deslineEdit.setStyleSheet(self.list_style_l)

        self.name.setFont(font)
        self.iplineEdit.setFont(font)
        self.netmask.setFont(font)
        self.deslineEdit.setFont(font)

        btn1.setStyleSheet(self.list_style_b)
        btn2.setStyleSheet(self.list_style_b)

        label1 = QLabel("name:")
        label2 = QLabel("ip:")

        label3 = QLabel("netmask:")
        label4 = QLabel("descripition:")

        label1.setFont(font)
        label2.setFont(font)
        label3.setFont(font)
        label4.setFont(font)

        self.iplineEdit.setInputMask('000.000.000.000;_')
        self.netmask.setInputMask('000.000.000.000;_')

        gridLayout.addWidget(label1, 0, 0, 1, 1)
        gridLayout.addWidget(self.name, 0, 1, 1, 1)
        gridLayout.addWidget(label2, 1, 0, 1, 1)
        gridLayout.addWidget(self.iplineEdit, 1, 1, 1, 1)
        gridLayout.addWidget(label3, 2, 0, 1, 1)
        gridLayout.addWidget(self.netmask, 2, 1,1,1)
        gridLayout.addWidget(label4, 3, 0, 1, 1)
        gridLayout.addWidget(self.deslineEdit, 3, 1, 1, 1)
        gridLayout.addWidget(btn1,4,0,1,1)
        gridLayout.addWidget(btn2,4,1,1,1)
        # buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        # gridLayout.addWidget(buttons,4,0,1,1)

        self.setLayout(gridLayout)

        # buttons.accepted.connect(self.accept)
        # buttons.rejected.connect(self.reject)
        btn2.clicked.connect(self.close)
        btn1.clicked.connect(self.line_get_text)

    def line_get_text(self):
        # self.flag=1
        data_str1=self.name.text()
        data_str2=self.iplineEdit.text()
        data_str3=self.netmask.text()
        data_str4=self.deslineEdit.text()
        self._datasinal.emit(data_str1,data_str2,data_str3,data_str4)
        print(self.name.text())
        print(self.iplineEdit.text())
        print(self.netmask.text())
        print(self.deslineEdit.text())
        self.close()
    # @staticmethod
    # def getData(parent=None):
    #     dialog=inputDialog()
    #     result=dialog.exec()
    #     print(result)
    #     print(type(result))
    #     print(QDialog.Accepted)
    #     print(type(QDialog))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    dia = inputDialog()
    dia.show()
    sys.exit(app.exec_())
