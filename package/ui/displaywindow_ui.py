# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\displaywindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DisplayWindow(object):
    def setupUi(self, DisplayWindow):
        DisplayWindow.setObjectName("DisplayWindow")
        DisplayWindow.resize(618, 441)
        DisplayWindow.setMinimumSize(QtCore.QSize(618, 441))
        DisplayWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        self.verticalLayout = QtWidgets.QVBoxLayout(DisplayWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(DisplayWindow)
        self.widget.setMinimumSize(QtCore.QSize(596, 25))
        self.widget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.home = QtWidgets.QPushButton(self.widget)
        self.home.setObjectName("home")
        self.horizontalLayout_2.addWidget(self.home)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.verticalLayout.addWidget(self.widget)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.OpenHeader = QtWidgets.QPushButton(DisplayWindow)
        self.OpenHeader.setFocusPolicy(QtCore.Qt.NoFocus)
        self.OpenHeader.setObjectName("OpenHeader")
        self.horizontalLayout.addWidget(self.OpenHeader)
        self.pushButton = QtWidgets.QPushButton(DisplayWindow)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.progressBar = QtWidgets.QProgressBar(DisplayWindow)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DisplayWindow)
        QtCore.QMetaObject.connectSlotsByName(DisplayWindow)

    def retranslateUi(self, DisplayWindow):
        _translate = QtCore.QCoreApplication.translate
        DisplayWindow.setWindowTitle(_translate("DisplayWindow", "Form"))
        self.home.setText(_translate("DisplayWindow", "Home"))
        self.OpenHeader.setText(_translate("DisplayWindow", "Open Header"))
        self.pushButton.setText(_translate("DisplayWindow", "Save"))
