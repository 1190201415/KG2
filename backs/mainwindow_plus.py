# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow_plus.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1110, 886)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1110, 810))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.treeView = QtWidgets.QTreeView(self.tab_5)
        self.treeView.setGeometry(QtCore.QRect(0, 0, 141, 370))
        self.treeView.setStyleSheet("border: none;")
        self.treeView.setObjectName("treeView")
        self.treeView_3 = QtWidgets.QTreeView(self.tab_5)
        self.treeView_3.setGeometry(QtCore.QRect(0, 372, 141, 391))
        self.treeView_3.setStyleSheet("border: none;")
        self.treeView_3.setObjectName("treeView_3")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.tabWidget.addTab(self.tab_6, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(660, 610))
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scrollArea_3 = QtWidgets.QScrollArea(self.widget_2)
        self.scrollArea_3.setStyleSheet("border: none;")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_10 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_10.setGeometry(QtCore.QRect(0, 0, 164, 788))
        self.scrollAreaWidgetContents_10.setObjectName("scrollAreaWidgetContents_10")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_10)
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.comboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents_10)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_4.addWidget(self.comboBox)
        self.treeView_kg = QtWidgets.QTreeView(self.scrollAreaWidgetContents_10)
        self.treeView_kg.setStyleSheet("border: none;")
        self.treeView_kg.setObjectName("treeView_kg")
        self.verticalLayout_4.addWidget(self.treeView_kg)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_10)
        self.verticalLayout_5.addWidget(self.scrollArea_3)
        self.horizontalLayout.addWidget(self.widget_2)
        self.horizontalLayout.setStretch(1, 4)
        self.horizontalLayout.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1110, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action1_1 = QtWidgets.QAction(MainWindow)
        self.action1_1.setObjectName("action1_1")
        self.action1_2 = QtWidgets.QAction(MainWindow)
        self.action1_2.setObjectName("action1_2")
        self.action2_1 = QtWidgets.QAction(MainWindow)
        self.action2_1.setObjectName("action2_1")
        self.action2_2 = QtWidgets.QAction(MainWindow)
        self.action2_2.setObjectName("action2_2")
        self.action2_3 = QtWidgets.QAction(MainWindow)
        self.action2_3.setObjectName("action2_3")
        self.menu.addAction(self.action1_1)
        self.menu.addAction(self.action1_2)
        self.menu_2.addAction(self.action2_1)
        self.menu_2.addAction(self.action2_2)
        self.menu_2.addAction(self.action2_3)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.toolBar.addAction(self.action1_1)
        self.toolBar.addAction(self.action1_2)
        self.toolBar.addAction(self.action2_1)
        self.toolBar.addAction(self.action2_2)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "Tab 2"))
        self.menu.setTitle(_translate("MainWindow", "新建"))
        self.menu_2.setTitle(_translate("MainWindow", "导入"))
        self.menu_3.setTitle(_translate("MainWindow", "保存"))
        self.menu_4.setTitle(_translate("MainWindow", "退出"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action1_1.setText(_translate("MainWindow", "新建实体类型"))
        self.action1_2.setText(_translate("MainWindow", "新建关系类型"))
        self.action2_1.setText(_translate("MainWindow", "导入实体类型"))
        self.action2_2.setText(_translate("MainWindow", "导入关系类型"))
        self.action2_3.setText(_translate("MainWindow", "导入知识图谱"))
