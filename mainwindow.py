# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QueryByLick.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1009, 708)
        MainWindow.setMinimumSize(QtCore.QSize(1009, 708))
        MainWindow.setMaximumSize(QtCore.QSize(1009, 708))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.recordButton = QtWidgets.QPushButton(self.centralwidget)
        self.recordButton.setGeometry(QtCore.QRect(30, 630, 75, 23))
        self.recordButton.setObjectName("recordButton")
        self.stopRecordButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopRecordButton.setGeometry(QtCore.QRect(140, 630, 75, 23))
        self.stopRecordButton.setObjectName("stopRecordButton")
        self.recordTimeLabel = QtWidgets.QLabel(self.centralwidget)
        self.recordTimeLabel.setGeometry(QtCore.QRect(30, 610, 47, 13))
        self.recordTimeLabel.setObjectName("recordTimeLabel")
        self.midiFileList = QtWidgets.QListWidget(self.centralwidget)
        self.midiFileList.setGeometry(QtCore.QRect(20, 150, 191, 341))
        self.midiFileList.setObjectName("midiFileList")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(250, 50, 20, 551))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.tempoEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.tempoEdit.setGeometry(QtCore.QRect(30, 570, 113, 20))
        self.tempoEdit.setMaxLength(3)
        self.tempoEdit.setObjectName("tempoEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 550, 47, 13))
        self.label.setObjectName("label")
        self.midiInputSelector = QtWidgets.QComboBox(self.centralwidget)
        self.midiInputSelector.setGeometry(QtCore.QRect(20, 110, 191, 22))
        self.midiInputSelector.setObjectName("midiInputSelector")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 47, 13))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1009, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.recordButton.setText(_translate("MainWindow", "Record"))
        self.stopRecordButton.setText(_translate("MainWindow", "Stop"))
        self.recordTimeLabel.setText(_translate("MainWindow", "TextLabel"))
        self.label.setText(_translate("MainWindow", "Tempo"))
        self.label_2.setText(_translate("MainWindow", "Midi Input"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

