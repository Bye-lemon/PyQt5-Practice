# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serial.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from serial import Serial
import time

from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QPushButton, QComboBox, QLabel, QLineEdit, \
    QTextBrowser, QMenuBar, QStatusBar, QMainWindow, QMessageBox
from PyQt5.QtCore import QRect, QCoreApplication, QMetaObject, QThread, QDateTime, pyqtSignal

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Ui_MainWindows(object):
    def setupUi(self, MainWindows):
        MainWindows.setObjectName("MainWindows")
        MainWindows.resize(800, 506)
        self.centralwidget = QWidget(MainWindows)
        self.centralwidget.setObjectName("centralwidget")
        self.plot = QGraphicsView(self.centralwidget)
        self.plot.setGeometry(QRect(135, 0, 671, 461))
        self.plot.setObjectName("plot")
        self.open = QPushButton(self.centralwidget)
        self.open.setGeometry(QRect(30, 210, 75, 23))
        self.open.setObjectName("open")
        self.closebtn = QPushButton(self.centralwidget)
        self.closebtn.setGeometry(QRect(30, 260, 75, 23))
        self.closebtn.setObjectName("close")
        self.COM = QComboBox(self.centralwidget)
        self.COM.setGeometry(QRect(10, 50, 111, 22))
        self.COM.setObjectName("COM")
        self.COM.addItem("")
        self.COM.addItem("")
        self.COM.addItem("")
        self.COM.addItem("")
        self.COM.addItem("")
        self.COM.addItem("")
        self.COM.addItem("")
        self.COM.addItem("")
        self.COMlable = QLabel(self.centralwidget)
        self.COMlable.setGeometry(QRect(10, 30, 54, 12))
        self.COMlable.setObjectName("COMlable")
        self.baud = QLineEdit(self.centralwidget)
        self.baud.setGeometry(QRect(10, 140, 113, 20))
        self.baud.setObjectName("baud")
        self.baudlable = QLabel(self.centralwidget)
        self.baudlable.setGeometry(QRect(10, 120, 54, 12))
        self.baudlable.setObjectName("baudlable")
        self.output = QTextBrowser(self.centralwidget)
        self.output.setGeometry(QRect(10, 380, 111, 81))
        self.output.setObjectName("output")
        self.outputlabel = QLabel(self.centralwidget)
        self.outputlabel.setGeometry(QRect(10, 350, 54, 12))
        self.outputlabel.setObjectName("outputlabel")
        MainWindows.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindows)
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindows.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindows)
        self.statusbar.setObjectName("statusbar")
        MainWindows.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindows)
        QMetaObject.connectSlotsByName(MainWindows)

    def retranslateUi(self, MainWindows):
        _translate = QCoreApplication.translate
        MainWindows.setWindowTitle(_translate("MainWindows", "Serial Helper"))
        self.open.setText(_translate("MainWindows", "打开串口"))
        self.closebtn.setText(_translate("MainWindows", "关闭串口"))
        self.COM.setItemText(0, _translate("MainWindows", "COM1"))
        self.COM.setItemText(1, _translate("MainWindows", "COM2"))
        self.COM.setItemText(2, _translate("MainWindows", "COM3"))
        self.COM.setItemText(3, _translate("MainWindows", "COM4"))
        self.COM.setItemText(4, _translate("MainWindows", "COM5"))
        self.COM.setItemText(5, _translate("MainWindows", "COM6"))
        self.COM.setItemText(6, _translate("MainWindows", "COM7"))
        self.COM.setItemText(7, _translate("MainWindows", "COM8"))
        self.COMlable.setText(_translate("MainWindows", "COM口"))
        self.baudlable.setText(_translate("MainWindows", "波特率"))
        self.outputlabel.setText(_translate("MainWindows", "串口输出"))


class MyFigure(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='dimgrey')
        super(MyFigure, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)


class GUI(QMainWindow, Ui_MainWindows):
    def __init__(self):
        super(GUI, self).__init__()
        self.setupUi(self)
        self.scene = QGraphicsScene()
        self.data1 = [0 for i in range(10)]
        self.data2 = [0 for i in range(10)]
        self.data3 = [0 for i in range(10)]
        self.ser = Serial()
        self.open.clicked.connect(self.get_serial)
        self.closebtn.clicked.connect(self.close_serial)

    def get_serial(self):
        self.ser.port = self.COM.currentText()
        self.ser.baudrate = int(self.baud.text())
        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None

    def read_serial(self):
        out = self.ser.read(24)
        v1, v2, v3 = round((out[6] * 256 + out[7]) * 0.1, 2), round((out[14] * 256 + out[15]) * 0.1, 2), round(
            (out[22] * 256 + out[23]) * 0.1, 2)
        time.sleep(0.02)
        return v1, v2, v3

    def test_serial(self):
        return self.ser.read(2).decode('iso-8859-1')

    def update_gui(self):
        if self.ser.isOpen():
            self.open.setEnabled(False)
            self.closebtn.setEnabled(True)
            in1, in2, in3 = self.read_serial()
            self.output.setPlainText(str(in1) + ' MPa' + '\n' + str(in2) + ' MPa' + '\n' + str(in3) + ' MPa' + '\n')
            self.data1 = self.data1[1:]
            self.data1.append(in1)
            self.data2 = self.data2[1:]
            self.data2.append(in2)
            self.data3 = self.data3[1:]
            self.data3.append(in3)
            self.plot_serial()
        else:
            self.open.setEnabled(True)
            self.closebtn.setEnabled(False)

    def close_serial(self):
        self.ser.close()

    def plot_serial(self):
        t = [i / 10.0 for i in range(0, 10)]
        s1 = self.data1
        s2 = self.data2
        s3 = self.data3
        self.this_figure = MyFigure(width=6, height=4, dpi=100)
        self.this_figure.axes.grid('on')
        self.this_figure.axes.plot(t, s1)
        self.this_figure.axes.plot(t, s2)
        self.this_figure.axes.plot(t, s3)
        self.scene.addWidget(self.this_figure)
        self.plot.setScene(self.scene)
        self.plot.show()


class Backend(QThread):
    update_date = pyqtSignal(str)

    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            self.update_date.emit(str(data))
            time.sleep(1)
