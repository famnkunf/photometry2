# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\headerwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HeaderWindow(object):
    def setupUi(self, HeaderWindow):
        HeaderWindow.setObjectName("HeaderWindow")
        HeaderWindow.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(HeaderWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(HeaderWindow)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout.addWidget(self.textBrowser)
        self.verticalScrollBar = QtWidgets.QScrollBar(HeaderWindow)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.horizontalLayout.addWidget(self.verticalScrollBar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalScrollBar = QtWidgets.QScrollBar(HeaderWindow)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.verticalLayout.addWidget(self.horizontalScrollBar)

        self.retranslateUi(HeaderWindow)
        QtCore.QMetaObject.connectSlotsByName(HeaderWindow)

    def retranslateUi(self, HeaderWindow):
        _translate = QtCore.QCoreApplication.translate
        HeaderWindow.setWindowTitle(_translate("HeaderWindow", "Form"))
