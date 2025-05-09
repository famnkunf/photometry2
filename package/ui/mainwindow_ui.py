# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(616, 549)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(600, 500))
        MainWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setActivationOrder(QtWidgets.QMdiArea.CreationOrder)
        self.mdiArea.setViewMode(QtWidgets.QMdiArea.SubWindowView)
        self.mdiArea.setObjectName("mdiArea")
        self.verticalLayout_2.addWidget(self.mdiArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 616, 26))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Open = QtWidgets.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")
        self.actionHistogram = QtWidgets.QAction(MainWindow)
        self.actionHistogram.setObjectName("actionHistogram")
        self.actionCloseAll = QtWidgets.QAction(MainWindow)
        self.actionCloseAll.setObjectName("actionCloseAll")
        self.actionAperture = QtWidgets.QAction(MainWindow)
        self.actionAperture.setObjectName("actionAperture")
        self.actionObjects = QtWidgets.QAction(MainWindow)
        self.actionObjects.setObjectName("actionObjects")
        self.actionGraph = QtWidgets.QAction(MainWindow)
        self.actionGraph.setObjectName("actionGraph")
        self.actionTiled = QtWidgets.QAction(MainWindow)
        self.actionTiled.setObjectName("actionTiled")
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.actionCloseAll)
        self.menuWindow.addAction(self.actionHistogram)
        self.menuWindow.addAction(self.actionAperture)
        self.menuWindow.addAction(self.actionObjects)
        self.menuWindow.addAction(self.actionGraph)
        self.menuView.addAction(self.actionTiled)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        MainWindow.destroyed.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu_File.setTitle(_translate("MainWindow", "File"))
        self.menuWindow.setTitle(_translate("MainWindow", "Window"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.action_Open.setText(_translate("MainWindow", "Open"))
        self.actionHistogram.setText(_translate("MainWindow", "Histogram"))
        self.actionCloseAll.setText(_translate("MainWindow", "Close All"))
        self.actionAperture.setText(_translate("MainWindow", "Aperture"))
        self.actionObjects.setText(_translate("MainWindow", "Objects"))
        self.actionGraph.setText(_translate("MainWindow", "Graph"))
        self.actionTiled.setText(_translate("MainWindow", "Tiled"))
