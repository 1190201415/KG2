# -*-coding = utf-8 -*-
# @Time : 2024/2/2 15:18
# @Author :skq
# @File : backup.py
# @Software: PyCharm
# GUIdemo1.py
# Demo1 of GUI by PqYt5
# Copyright 2021 Youcans, XUPT
# Crated：2021-10-06
# encoding=utf-8
import copy
import gc
import os
import sys
import time

from PyQt5 import QtWidgets, QtCore

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, Qt, QCoreApplication, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget, \
    QListView, QProgressDialog, QHBoxLayout, QVBoxLayout, QSplitter, \
    QGraphicsScene, QApplication, QPushButton, QGraphicsView, QAbstractItemView

import Myclass
from Myclass import current_kg_name
from untitled import Ui_MainWindow
from new_entity import Ui_Form


class childwindow_1(QtWidgets.QWidget, Ui_Form):
    my_sign1 = pyqtSignal(str)

    def __init__(self, parent=None):
        super(childwindow_1, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.clickpushbutton)
        self.pushButton_2.clicked.connect(self.clickpushbutton_2)

    def clickpushbutton(self):
        name = self.lineEdit.text()
        self.my_sign1.emit(name)
        self.close()

    def clickpushbutton_2(self):
        self.close()


class my_MainWindow(QMainWindow, Ui_MainWindow):
    knowledge_graphs = {
        # "知识图谱1": {
        #     "entities": [],
        #     "relations": []
        # },
    }
    num = 1
    is_kg_changed = False

    def __init__(self, parent=None):
        super(my_MainWindow, self).__init__(parent)
        Myclass.init_meta_kg_dict()
        Myclass.change_meta_kg()  # 这两句放在最前面

        self.now_entity_type = None
        self.now_relation_type = None
        self.setupUi(self)
        self.setMinimumSize(0, 0)
        self.initentityType()
        self.initrelationType()
        self.init_treeview_1(self.treeView, Myclass.entityType_dict, Myclass.ktsqepType_dict, name='独立实体类型',
                             name2='附加实体类型')
        # self.init_treeview(self.treeView_2, self.KG_dict, name=' 计算思维（计算机科学导论）')
        # self.graphicsSence = Myclass.GraphicScene(parent=self.centralwidget)

        # 需要在class文件中修改这两句，很恶心（最好不要变动untitled。py，每次变都要改）
        # self.graphicsView = Myclass.GraphicView(parent=self.centralwidget, graphic_scene=self.graphicsSence)#
        # self.graphicsView.setGeometry(QtCore.QRect(225, 51, 661, 611))
        self.graphicsView.setObjectName("graphicsView")

        self.graphicsView.setSceneRect(0, 0, 5000, 5000)  # 设置场景大小
        self.graphicsView.setMinimumSize(0, 0)
        self.treeView_kg.my_sign_kg.connect(self.update_kg_treeview)
        self.treeView_kg.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.graphicsSence.setItemIndexMethod(QGraphicsScene.NoIndex)

        self.graphicsView.entityDropped.connect(self.setchange)
        self.graphicsSence.entityRemove.connect(self.setchange)
        self.graphicsView.relationAdded.connect(self.setchange)
        self.graphicsView.relationRemove.connect(self.setchange)
        self.graphicsView.move.connect(self.setchange)
        self.graphicsView.back_1.connect(self.back)
        self.graphicsSence.scenechanged.connect(self.setchange)

        self.init_treeview(self.treeView_3, Myclass.relationType_dict, name='关系类型列表')
        self.treeView.setDragEnabled(True)
        self.treeView_kg.setAcceptDrops(True)
        self.treeView.setDragDropMode(QListView.DragOnly)

        self.init_kg_treeview()
        self.treeView_kg.selectionModel().selectionChanged.connect(self.on_kg_selected)

        self.treeView.clicked.connect(self.clicked_treeView)
        self.treeView_3.clicked.connect(self.clicked_treeView3)

        self.action1_1.triggered.connect(self.clickaction1_1)
        self.action1_2.triggered.connect(self.save_file)
        self.action1_3.triggered.connect(self.copy_kg)
        self.action1_4.triggered.connect(self.another_save_file)
        self.action1_5.triggered.connect(self.choosedir)
        self.action1_6.triggered.connect(self.openfile)
        self.action1_7.triggered.connect(self.opendir)
        self.action1_8.triggered.connect(self.change_name)

        self.action2_1.triggered.connect(self.confirm_auto_layout)
        self.action2_2.triggered.connect(self.save_as_picture)

        self.action3_1.triggered.connect(self.set_mouse)
        self.action3_2.triggered.connect(self.start_drag)
        self.graphicsView.updateRequest.connect(self.handle_update_request)
        # self.graphicsSence.changed.connect(self.setchange)
        # self.initLayouts()
        # self.showMaximized()
        self.setWindowTitle('KT-SQEP知识图谱工具')
        Myclass.readfilepath = self.treeView_kg.special_initxml()
        self.update_kg_treeview(text=Myclass.readfilepath)
        # self.init_comboBox_2()
        self.init_tabwidegt()

        self.combox_init()
        self.comboBox.currentIndexChanged.connect(self.combox_change)

        # self.backbtn = QPushButton(self.graphicsView)
        # self.backbtn.resize(60, 35)
        # pos = self.graphicsView.pos()
        # self.backbtn.setText('回退')
        # self.backbtn.move(pos)
        # self.backbtn.clicked.connect(self.back)

        self.graphicsSence.update_kg()

    def combox_init(self, text=None):
        self.comboBox.blockSignals(True)
        self.comboBox.clear()
        list = copy.deepcopy(Myclass.history)
        self.comboBox.addItems(list)
        list_name = []
        num_items = self.comboBox.count()

        # Read and print all items
        for index in range(num_items):
            item_text = self.comboBox.itemText(index)
            list_name.append(item_text)
        if text is None:
            self.comboBox.blockSignals(False)
            return
        f, n = self.file_in(text, list_name)
        if text is not None and f:
            self.comboBox.setCurrentText(n)

        self.comboBox.blockSignals(False)

    def combox_change(self):
        a = self.comboBox.currentText()
        Myclass.readfilepath = a
        self.asave_kgs()
        Myclass.knowledge_graphs_class.clear()
        self.treeView_kg.initxml(a)
        self.update_kg_treeview(text=a)
        self.graphicsSence.update_kg()
        if len(Myclass.knowledge_graphs_class.keys()) == 0:
            self.handle_my_sign1(name='未命名')

    def back(self):
        path = os.path.join('./.produrce', Myclass.current_kg_name + '.xml')
        print(path)
        if (os.path.exists(path)):
            self.treeView_kg.readfile(path)
            self.setchange()
            print('读取成功')
        return

    def setchange(self):
        print('setchange')
        if self.treeView_kg.myreadfile:
            return
        name = Myclass.current_kg_name
        if Myclass.knowledge_graphs_class[name]['is_change'] == True:
            return
        Myclass.knowledge_graphs_class[name]['is_change'] = True
        self.update_kg_treeview(Myclass.readfilepath)

    def save_as_picture(self):
        reply = QMessageBox.question(self, '保存为图片', '确认保存？', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.graphicsView.save_as_picture(path='./Screenshot')
        else:
            return

    def file_in(self, file, list):
        for i in list:
            if os.path.samefile(file, i):
                return True, i
        return False, None

    def openfile(self):
        m = QtWidgets.QFileDialog.getOpenFileName(None, "文件读取", '', 'xml 文件(*.xml)', )  # 起始路径
        if m[0] == '':
            return
        dirname, full_name = os.path.split(m[0])
        if os.path.samefile(dirname, Myclass.readfilepath):
            self.treeView_kg.readfile(m[0])
        else:
            self.asave_kgs()
            Myclass.knowledge_graphs_class.clear()
            self.treeView_kg.readfile(m[0])
            Myclass.readfilepath = dirname
            f, n = self.file_in(dirname, Myclass.history)
            if not f:
                Myclass.history.append(dirname)
            self.combox_init(dirname)
            self.update_kg_treeview(text=dirname)
            self.graphicsSence.update_kg()
            if len(Myclass.knowledge_graphs_class.keys()) == 0:
                self.handle_my_sign1(name='未命名')

    def opendir(self):  # 这个是读到当前目录还是新建一个目录？
        m = QtWidgets.QFileDialog.getExistingDirectory(None, "文件夹读取", )  # 起始路径
        if m == '':
            return
        Myclass.readfilepath = m
        f, n = self.file_in(m, Myclass.history)
        if not f:
            Myclass.history.append(m)
        self.asave_kgs()
        Myclass.knowledge_graphs_class.clear()
        self.treeView_kg.initxml(m)
        self.combox_init(m)
        self.update_kg_treeview(text=m)
        self.graphicsSence.update_kg()
        if len(Myclass.knowledge_graphs_class.keys()) == 0:
            self.handle_my_sign1(name='未命名')

    def choosedir(self):
        m = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹或新建文件夹保存", )  # 起始路径
        if m == '':
            print("没选，返回")
            return
        Myclass.save_kgs(dir=m)

    def start_drag(self):
        self.graphicsView.drag_flag = 1

    def another_save(self):
        Myclass.other_save_kg(parent=self)

    def meta_dict_name_changed(self, name):
        self.graphicsSence.update_kg()
        self.asave_kgs()
        self.csave_kgs()
        Myclass.save_meta_kg()
        Myclass.current_meta_kg_dict = name
        Myclass.change_meta_kg()
        self.cleartreeview(self.treeView)
        self.cleartreeview(self.treeView_3)
        self.init_treeview_1(self.treeView, Myclass.entityType_dict, Myclass.ktsqepType_dict, name='独立实体类型',
                             name2='附加实体类型')
        self.update_kg_treeview(Myclass.readfilepath)
        self.combox_init(Myclass.readfilepath)
        self.init_treeview(self.treeView_3, Myclass.relationType_dict, name='关系类型列表')
        self.graphicsSence.update_kg()
        if Myclass.current_kg_name == '知识图谱1' and Myclass.current_kg_name not in Myclass.knowledge_graphs_class.keys():
            self.handle_my_sign1(name='未命名')
        print(name)

    def init_tabwidegt(self):
        _translate = QtCore.QCoreApplication.translate
        # self.comboBox_2.currentIndexChanged.connect(self.comboBox_2_changed)
        # for i in Myclass.meta_dict.keys():
        #     self.comboBox_2.addItems([i])
        self.placeholder = QWidget()
        self.tabWidget.addTab(self.widget, "教学知识图谱")
        self.tabWidget.addTab(self.placeholder, "能力知识图谱")
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

        # 初始化显示第一个 tab 的内容
        # self.on_tab_changed(0)
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("MainWindow", "Tab 1"))

    def on_tab_changed(self, index):
        self.tabWidget.blockSignals(True)
        name = self.tabWidget.tabText(index)
        print(name)
        for i in range(self.tabWidget.count()):
            self.tabWidget.removeTab(i)
        if name == '教学知识图谱':
            self.tabWidget.addTab(self.widget, "教学知识图谱")
            self.tabWidget.addTab(self.placeholder, "能力知识图谱")
        else:
            self.tabWidget.addTab(self.placeholder, "教学知识图谱")
            self.tabWidget.addTab(self.widget, "能力知识图谱")
        self.meta_dict_name_changed(name)
        self.tabWidget.setCurrentIndex(index)
        self.tabWidget.blockSignals(False)

    def copy_kg(self):
        print(1)
        self.childwindow2 = childwindow_1()
        print(2)
        self.childwindow2.changename(text='输入新的图谱名称')

        self.childwindow2.my_sign1.connect(self.handle_my_sign2)
        print(3)
        self.childwindow2.show()
        print(4)

    def set_mouse(self):
        self.graphicsView.draw_link_flag = 0
        self.graphicsView.drag_flag = 0
        if self.graphicsView.drag_link is not None:
            self.graphicsView.drag_link.remove()
            self.graphicsView.drag_link = None
        self.graphicsView.setCursor(Qt.ArrowCursor)

    def initLayouts(self):
        # 创建主布局容器
        mainLayout = QHBoxLayout()

        # 创建左侧、中间和右侧的布局容器
        leftLayout = QVBoxLayout()
        middleLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()

        # 向左侧布局添加组件
        leftLayout.addWidget(self.treeView)
        leftLayout.addWidget(self.treeView_3)

        # 向中间布局添加组件
        middleLayout.addWidget(self.graphicsView)

        # 向右侧布局添加组件
        rightLayout.addWidget(self.treeView_kg)

        # 使用QSplitter来实现可调节的分割
        splitter = QSplitter(Qt.Horizontal)

        # 创建三个小部件，分别为左侧、中间和右侧布局的容器
        leftWidget = QWidget()
        middleWidget = QWidget()
        rightWidget = QWidget()

        # 将各自的布局设置给对应的小部件
        leftWidget.setLayout(leftLayout)
        middleWidget.setLayout(middleLayout)
        rightWidget.setLayout(rightLayout)

        # 将小部件添加到分割器
        splitter.addWidget(leftWidget)
        splitter.addWidget(middleWidget)
        splitter.addWidget(rightWidget)

        # 可以通过setStretchFactor调整各部分的初始比例
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 1)

        # 将分割器添加到主布局
        mainLayout.addWidget(splitter)
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        # 应用主布局
        self.centralWidget.setLayout(mainLayout)

    def clicked_treeView3(self):
        index = self.treeView_3.currentIndex()
        text = self.treeView_3.model().data(index)
        print(text)
        if text == '包含关系':
            self.graphicsView.draw_link_flag = 1
            self.graphicsView.setCursor(Qt.DragLinkCursor)
        if '次序关系' in text:
            self.graphicsView.draw_link_flag = 2
            self.graphicsView.setCursor(Qt.DragLinkCursor)
        if text == '连接资源':
            self.graphicsView.draw_link_flag = 3
            self.graphicsView.setCursor(Qt.DragLinkCursor)
        if '关键次序' in text:
            self.graphicsView.draw_link_flag = 4
            self.graphicsView.setCursor(Qt.DragLinkCursor)
        if text == '落实关系':
            self.graphicsView.draw_link_flag = 8
            self.graphicsView.setCursor(Qt.DragLinkCursor)

    def clicked_treeView(self):
        index = self.treeView.currentIndex()
        text = self.treeView.model().data(index)
        print(text)

    def init_ab_treeview_1(self, treeView, dict, dict2, name, name2):
        model = QtGui.QStandardItemModel()
        entityytpeclass1 = QtGui.QStandardItem(name)
        entityytpeclass2 = QtGui.QStandardItem(name2)
        item1 = QtGui.QStandardItem('内容型')
        item2 = QtGui.QStandardItem('资源型')
        item3 = QtGui.QStandardItem('方法型')
        entityytpeclass1.appendRow(item1)
        entityytpeclass1.appendRow(item2)
        entityytpeclass2.appendRow(item3)
        num = 0
        f = 0
        for i in dict.keys():
            if num < 5:
                item = QtGui.QStandardItem(dict[i].class_name)
                # item.setIcon(QIcon('picture/' + dict[i].class_name + '.png'))
                item1.appendRow(item)
                num = num + 1
            else:
                item = QtGui.QStandardItem(dict[i].class_name)
                # item.setIcon(QIcon('picture/' + dict[i].class_name + '.png'))
                item2.appendRow(item)
                num = num + 1
        for i in dict2.keys():
            if 'L' in dict2[i].class_name and f == 0:
                item = QtGui.QStandardItem('能力等级L1')
                f = 1
            elif 'L' in dict2[i].class_name and f == 1:
                continue
            # item.setIcon(QIcon('picture/' + dict2[i].class_name + '.png'))
            else:
                item = QtGui.QStandardItem(dict2[i].class_name)
            item3.appendRow(item)

        model.appendRow(entityytpeclass1)
        model.appendRow(entityytpeclass2)

        treeView.setModel(model)
        model.setHorizontalHeaderLabels([''])
        treeView.expandAll()
        # 03/21：初始化右侧树视图

    def init_treeview_1(self, treeView, dict, dict2, name='', name2=''):
        treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        treeView.setHeaderHidden(True)
        if Myclass.current_meta_kg_dict == '能力知识图谱':
            self.init_ab_treeview_1(treeView, dict, dict2, name, name2)
            return
        model = QtGui.QStandardItemModel()
        entityytpeclass1 = QtGui.QStandardItem(name)
        entityytpeclass2 = QtGui.QStandardItem(name2)
        item1 = QtGui.QStandardItem('内容型')
        item2 = QtGui.QStandardItem('资源型')
        item3 = QtGui.QStandardItem('方法型')
        entityytpeclass1.appendRow(item1)
        entityytpeclass1.appendRow(item2)
        entityytpeclass2.appendRow(item3)
        num = 0
        for i in dict.keys():
            if num < 4:
                item = QtGui.QStandardItem(dict[i].class_name)
                item.setIcon(QIcon('picture/' + dict[i].class_name + '.png'))
                item1.appendRow(item)
                num = num + 1
            else:
                item = QtGui.QStandardItem(dict[i].class_name)
                item.setIcon(QIcon('picture/' + dict[i].class_name + '.png'))
                item2.appendRow(item)
                num = num + 1
        for i in dict2.keys():
            item = QtGui.QStandardItem(dict2[i].class_name)
            item.setIcon(QIcon('picture/' + dict2[i].class_name + '.png'))
            item3.appendRow(item)

        model.appendRow(entityytpeclass1)
        model.appendRow(entityytpeclass2)

        treeView.setModel(model)
        model.setHorizontalHeaderLabels([''])
        treeView.expandAll()
        # 03/21：初始化右侧树视图

    def init_treeview(self, treeView, dict, name=''):
        treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        treeView.setHeaderHidden(True)
        model = QtGui.QStandardItemModel()
        entityytpeclass1 = QtGui.QStandardItem(name)
        for i in dict.keys():
            item = QtGui.QStandardItem(dict[i].class_name)
            item.setIcon(QIcon('picture/' + dict[i].class_name + '.png'))
            entityytpeclass1.appendRow(item)
        model.appendRow(entityytpeclass1)
        for i in range(model.rowCount()):
            print(model.item(i))
        treeView.setModel(model)
        model.setHorizontalHeaderLabels([''])
        treeView.expandAll()
        # 03/21：初始化右侧树视图

    def init_kg_treeview(self):
        # 创建模型
        self.model_kg = QtGui.QStandardItemModel()
        self.model_kg.setHorizontalHeaderLabels([''])
        self.treeView_kg.setModel(self.model_kg)
        self.treeView_kg.setHeaderHidden(True)

        # 添加数据示例
        root_item = QtGui.QStandardItem(" 计算思维（计算机科学导论）")
        self.model_kg.appendRow(root_item)

        # 示例：添加几个知识图谱

        # for i in range(1, 2):
        #     kg_item = QtGui.QStandardItem(f"知识图谱{i}")
        #     root_item.appendRow(kg_item)
        self.treeView_kg.expandAll()

        # # 为每个知识图谱添加实体和关系列表
        # entities_item = QtGui.QStandardItem("实体列表")
        # relations_item = QtGui.QStandardItem("关系列表")
        # kg_item.appendRow(entities_item)
        # kg_item.appendRow(relations_item)

        # 示例：为每个列表添加几个条目
        # for j in range(1, 3):
        #     entities_item.appendRow(QtGui.QStandardItem(f"实体{j}"))
        #     relations_item.appendRow(QtGui.QStandardItem(f"关系{j}"))

    def cleartreeview(self, treeview):
        model = treeview.model()

        for i in range(model.rowCount()):
            # for j in range(model.item(i).rowCount()):
            #     model.item(i).removeRow(j)
            model.removeRow(i)

    def update_kg_treeview(self, text=' 计算思维（计算机科学导论）'):
        text = Myclass.readfilepath
        for i in range(self.model_kg.rowCount()):
            for j in range(self.model_kg.item(i).rowCount()):
                self.model_kg.item(i).removeRow(j)
            self.model_kg.removeRow(i)
        # 添加数据示例
        root_item = QtGui.QStandardItem(text)
        self.model_kg.appendRow(root_item)

        for i in Myclass.knowledge_graphs_class.keys():
            kg_item = QtGui.QStandardItem(i)
            root_item.appendRow(kg_item)
            if Myclass.knowledge_graphs_class[i]['is_change']:
                kg_item.setIcon(self.create_dot_icon())
        self.treeView_kg.expandAll()

        # # 为每个知识图谱添加实体和关系列表
        # entities_item = QtGui.QStandardItem("实体列表")
        # relations_item = QtGui.QStandardItem("关系列表")
        # kg_item.appendRow(entities_item)
        # kg_item.appendRow(relations_item)

        # 示例：为每个列表添加几个条目
        # for j in range(1, 3):
        #     entities_item.appendRow(QtGui.QStandardItem(f"实体{j}"))
        #     relations_item.appendRow(QtGui.QStandardItem(f"关系{j}"))

    def create_dot_icon(self):
        # 创建一个带点的图标
        pixmap = QPixmap(10, 10)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setBrush(Qt.red)
        painter.drawEllipse(0, 0, 10, 10)
        painter.end()

        return QIcon(pixmap)

    def click_kg_treeview_selected(self):
        # 获取当前选中的项
        index = self.treeView_kg.currentIndex()
        item = self.model_kg.itemFromIndex(index)
        self.graphicsSence.update_kg()
        print(f"当前选中的项：{item.text()}")
        # 在这里可以根据选中的项进行进一步的操作

    def handle_update_request(self):
        self.graphicsSence.update_kg()
        self.graphicsSence.update()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        # if self.graphicsSence.is_kg_changed:
        # for i in Myclass.knowledge_graphs_class.keys():
        #     if Myclass.knowledge_graphs_class[i]['is_change']:
        #         reply = QMessageBox.question(self, '保存更改', '是否保存  '+i+'   更新?', QMessageBox.Yes | QMessageBox.No,
        #                                      QMessageBox.Yes)
        #         if reply == QMessageBox.Yes:
        #             NUM_FUN = 5
        #             self.progressDialog = QProgressDialog('保存进度', None, 0, NUM_FUN, self)
        #             self.progressDialog.setWindowTitle("退出中")
        #             self.progressDialog.setWindowFlags((self.progressDialog.windowFlags() & ~Qt.WindowCloseButtonHint))
        #             self.progressDialog.show()
        #             self.save_file(name=i)
        #             self.progressDialog.setValue(NUM_FUN)
        self.graphicsSence.update_kg()
        self.asave_kgs()
        self.csave_kgs()
        reply = QMessageBox.question(self, '退出', '确认退出？', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            a0.accept()

        else:
            a0.ignore()

    def save_file(self, name=None):
        self.graphicsView.remove_drag_link()
        self.graphicsSence.update()
        if name is None or type(name) == bool:
            KG = Myclass.current_kg_name
        else:
            KG = name
        print("KGS" + KG)
        if KG not in Myclass.knowledge_graphs_class.keys():
            return
        self.graphicsSence.update_kg()
        Myclass.save_kg(name=KG, kg=Myclass.knowledge_graphs_class[KG],
                        dir=Myclass.knowledge_graphs_class[KG]['save_dir'])
        Myclass.knowledge_graphs_class[KG]['is_change'] = False
        self.update_kg_treeview()

    def another_save_file(self):
        m = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹或新建文件夹保存", )  # 起始路径
        if m == '':
            print("没选，返回")
            return
        KG = Myclass.current_kg_name
        if KG not in Myclass.knowledge_graphs_class.keys():
            return
        Myclass.knowledge_graphs_class[KG]['save_dir'] = m
        Myclass.save_kg(name=KG, kg=Myclass.knowledge_graphs_class[KG], dir=m)
        Myclass.knowledge_graphs_class[KG]['is_change'] = False
        self.update_kg_treeview()

    def asave_kgs(self):
        for i in Myclass.knowledge_graphs_class.keys():
            if Myclass.knowledge_graphs_class[i]['is_change']:
                reply = QMessageBox.question(self, '保存更改', '是否保存  ' + i + '   更新?', QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    NUM_FUN = 5
                    self.progressDialog = QProgressDialog('保存进度', None, 0, NUM_FUN, self)
                    self.progressDialog.setWindowTitle("退出中")
                    self.progressDialog.setWindowFlags((self.progressDialog.windowFlags() & ~Qt.WindowCloseButtonHint))
                    self.progressDialog.show()
                    self.save_file(name=i)
                    self.progressDialog.setValue(NUM_FUN)

    def csave_kgs(self):
        self.graphicsSence.update()
        for KG in Myclass.knowledge_graphs_class.keys():
            print('保存kg：', KG)
            Myclass.save_kg(name=KG, kg=Myclass.knowledge_graphs_class[KG], dir='./temp')
            pass

    def confirm_auto_layout(self):
        reply = QMessageBox.question(
            self, '确认自动布局', '您确定要执行自动布局吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.auto_layout()
            Myclass.knowledge_graphs_class[Myclass.current_kg_name]['is_change'] = True
            self.update_kg_treeview()

    def auto_layout(self):
        point = self.graphicsView.get_view_left_middle()
        self.graphicsSence.auto_layout(point)

    def abilityinitrelationType(self):
        abidict: Myclass.meta_kg
        abidict = Myclass.meta_dict['能力知识图谱']
        abidict.relationType_dict['abLineType1'] = Myclass.relationType(class_name='包含关系', mask='知识连线',
                                                                        classification='包含关系',
                                                                        head_need='内容方法型节点', tail_need='内容方法型节点')
        abidict.relationType_dict['abLineType2'] = Myclass.relationType(class_name='次序关系', mask='知识连线',
                                                                        classification='次序关系',
                                                                        head_need='内容方法型节点', tail_need='内容方法型节点')
        abidict.relationType_dict['abLineType4'] = Myclass.relationType(class_name='关键次序', mask='知识连线',
                                                                        classification='次序关系',
                                                                        head_need='内容方法型节点', tail_need='内容方法型节点')
        abidict.relationType_dict['abLineType8'] = Myclass.relationType(class_name='落实关系', mask='知识连线',
                                                                        classification='落实关系',
                                                                        head_need='内容方法型节点', tail_need='内容方法型节点')
        return

    def abilityinitentityType(self):
        abidict: Myclass.meta_kg
        abidict = Myclass.meta_dict['能力知识图谱']
        cwd = os.getcwd()
        path = os.path.join(cwd, 'xml')
        abidict.readfilepath = path
        abidict.entityType_dict['abNodeType1'] = Myclass.entityType(class_name='能力领域:CA', classification='内容方法型节点',
                                                                    identity='知识',
                                                                    level='一级', opentool='无')
        abidict.entityType_dict['abNodeType2'] = Myclass.entityType(class_name='能力单元:CU', classification='内容方法型节点',
                                                                    identity='知识',
                                                                    level='二级', opentool='无')
        abidict.entityType_dict['abNodeType3'] = Myclass.entityType(class_name='能力点:CP', classification='内容方法型节点',
                                                                    identity='知识',
                                                                    level='归纳级', opentool='无')
        abidict.entityType_dict['abNodeType4'] = Myclass.entityType(class_name='学生任务:SJ', classification='内容方法型节点',
                                                                    identity='知识',
                                                                    level='内容级', opentool='无')
        abidict.entityType_dict['abNodeType5'] = Myclass.entityType(class_name='知识点:KP', classification='内容方法型节点',
                                                                    identity='知识',
                                                                    level='内容级', opentool='无')
        abidict.ktsqepType_dict["NodeType1"] = Myclass.entityType(class_name='能力等级L1', classification='附加节点',
                                                                  identity='能力点',
                                                                  level='三级', opentool='无')
        abidict.ktsqepType_dict["NodeType2"] = Myclass.entityType(class_name='能力等级L2', classification='附加节点',
                                                                  identity='能力点',
                                                                  level='三级', opentool='无')
        abidict.ktsqepType_dict["NodeType3"] = Myclass.entityType(class_name='能力等级L3', classification='附加节点',
                                                                  identity='能力点',
                                                                  level='三级', opentool='无')
        abidict.ktsqepType_dict["NodeType4"] = Myclass.entityType(class_name='能力等级L4', classification='附加节点',
                                                                  identity='能力点',
                                                                  level='三级', opentool='无')
        abidict.ktsqepType_dict["NodeType5"] = Myclass.entityType(class_name='能力等级L5', classification='附加节点',
                                                                  identity='能力点',
                                                                  level='三级', opentool='无')
        abidict.ktsqepType_dict["NodeType6"] = Myclass.entityType(class_name='能力等级L6', classification='附加节点',
                                                                  identity='能力点',
                                                                  level='三级', opentool='无')
        abidict.ktsqepType_dict["NodeType7"] = Myclass.entityType(class_name='能力等级L7', classification='附加节点',
                                                                  identity='能力点',
                                                                  level='三级', opentool='无')
        abidict.ktsqepType_dict["NodeType8"] = Myclass.entityType(class_name='能力等级L8', classification='附加节点',
                                                                  identity='能力点',
                                                                  level='三级', opentool='无')
        abidict.ktsqepType_dict["NodeType9"] = Myclass.entityType(class_name='能力等级L9', classification='附加节点',
                                                                  identity='能力点',
                                                                  level='三级', opentool='无')
        abidict.ktsqepType_dict["NodeType10"] = Myclass.entityType(class_name='项目级任务Pj', classification='附加节点',
                                                                   identity='学生任务',
                                                                   level='三级', opentool='无')
        abidict.ktsqepType_dict["NodeType11"] = Myclass.entityType(class_name='任务级任务Tk', classification='附加节点',
                                                                   identity='学生任务',
                                                                   level='三级', opentool='无')
        # abidict.entityType_dict['abNodeType4'] = Myclass.entityType(class_name='项目', classification='内容方法型节点',
        #                                                           identity='知识',
        #                                                           level='内容级', opentool='无')
        # abidict.entityType_dict['abNodeType5'] = Myclass.entityType(class_name='任务', classification='内容方法型节点',
        #                                                           identity='知识',
        #                                                           level='内容级', opentool='无')
        # abidict.entityType_dict['abNodeType6'] = Myclass.entityType(class_name='知识点', classification='内容方法型节点',
        #                                                           identity='知识',
        #                                                           level='内容级', opentool='无')
        return

    def initrelationType(self):
        cwd = os.getcwd()
        path = os.path.join(cwd, 'xml')
        Myclass.readfilepath = path
        Myclass.relationType_dict["LineType1"] = Myclass.relationType(class_name='包含关系', mask='知识连线',
                                                                      classification='包含关系',
                                                                      head_need='内容方法型节点', tail_need='内容方法型节点')
        Myclass.relationType_dict["LineType2"] = Myclass.relationType(class_name='次序：次序关系', mask='知识连线',
                                                                      classification='次序关系',
                                                                      head_need='内容方法型节点', tail_need='内容方法型节点')
        Myclass.relationType_dict["LineType4"] = Myclass.relationType(class_name='次序：关键次序', mask='知识连线',
                                                                      classification='次序关系',
                                                                      head_need='内容方法型节点', tail_need='内容方法型节点')
        Myclass.relationType_dict["LineType3"] = Myclass.relationType(class_name='连接资源', mask='知识—资源连线',
                                                                      classification='连接资源',
                                                                      head_need='内容方法型节点', tail_need='资源型节点')

        self.abilityinitrelationType()

    def initentityType(self):
        Myclass.entityType_dict["NodeType1"] = Myclass.entityType(class_name='知识领域:KA', classification='内容方法型节点',
                                                                  identity='知识',
                                                                  level='一级', opentool='无')
        Myclass.entityType_dict["NodeType2"] = Myclass.entityType(class_name='知识单元:KU', classification='内容方法型节点',
                                                                  identity='知识',
                                                                  level='二级', opentool='无')
        Myclass.entityType_dict["NodeType3"] = Myclass.entityType(class_name='知识点:KP', classification='内容方法型节点',
                                                                  identity='知识',
                                                                  level='归纳级', opentool='无')
        Myclass.entityType_dict["NodeType4"] = Myclass.entityType(class_name='关键知识细节:KD', classification='内容方法型节点',
                                                                  identity='知识',
                                                                  level='内容级', opentool='无')
        Myclass.entityType_dict["NodeType5"] = Myclass.entityType(class_name='视频:VD', classification='资源型节点',
                                                                  identity='Video',
                                                                  level='微课', opentool='Mvideo.exe')
        Myclass.entityType_dict["NodeType6"] = Myclass.entityType(class_name='PPT:PT', classification='资源型节点',
                                                                  identity='PPT',
                                                                  level='练习题', opentool='Powpoint.exe')
        Myclass.entityType_dict["NodeType7"] = Myclass.entityType(class_name='文档:PD', classification='资源型节点',
                                                                  identity='PDF',
                                                                  level='教学素材', opentool='PDFviewer')
        Myclass.ktsqepType_dict["NodeType1"] = Myclass.entityType(class_name='知识 K', classification='附加节点',
                                                                  identity='知识',
                                                                  level='三级', opentool='无')
        Myclass.ktsqepType_dict["NodeType2"] = Myclass.entityType(class_name='思维 T', classification='附加节点',
                                                                  identity='思维',
                                                                  level='三级', opentool='无')
        Myclass.ktsqepType_dict["NodeType3"] = Myclass.entityType(class_name='示例 E', classification='附加节点',
                                                                  identity='示例',
                                                                  level='三级', opentool='无')
        Myclass.ktsqepType_dict["NodeType4"] = Myclass.entityType(class_name='问题 Q', classification='附加节点',
                                                                  identity='问题',
                                                                  level='三级', opentool='无')
        Myclass.ktsqepType_dict["NodeType5"] = Myclass.entityType(class_name='练习 P', classification='附加节点',
                                                                  identity='练习',
                                                                  level='三级', opentool='无')
        Myclass.ktsqepType_dict["NodeType6"] = Myclass.entityType(class_name='思政 Z', classification='附加节点',
                                                                  identity='思政',
                                                                  level='三级', opentool='无')
        self.abilityinitentityType()

    def name_exists(self, name):
        if name in Myclass.knowledge_graphs_class.keys():
            return True
        return False

    def clickaction1_1(self):
        counter = 1
        name = '未命名'
        while self.name_exists(name):
            name = f"未命名_{counter}"
            counter += 1

        self.handle_my_sign1(name)

    def insert_EntityType(self, name, class_name='实体类型列表'):
        model = self.treeView.model()
        for i in range(model.rowCount()):
            m_name = model.item(i).text()
            if m_name == class_name:
                model.item(i).appendRow(QtGui.QStandardItem(name))

    def change_name(self):
        self.graphicsSence.update_kg()
        n = Myclass.current_kg_name
        reply = QMessageBox.question(self, '保存更改', '是否保存  ' + n + '   更新?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            NUM_FUN = 5
            self.progressDialog = QProgressDialog('保存进度', None, 0, NUM_FUN, self)
            self.progressDialog.setWindowTitle("退出中")
            self.progressDialog.setWindowFlags((self.progressDialog.windowFlags() & ~Qt.WindowCloseButtonHint))
            self.progressDialog.show()
            self.save_file(name=n)
            self.progressDialog.close()
        self.windows1 = childwindow_1()
        self.windows1.my_sign1.connect(self.rename)
        self.windows1.show()

    def rename(self, name):
        n = Myclass.current_kg_name
        if name not in Myclass.knowledge_graphs_class.keys():
            Myclass.knowledge_graphs_class[name] = Myclass.knowledge_graphs_class.pop(n)
            Myclass.knowledge_graphs_class[name]['is_change'] = True
            self.update_kg_treeview()

    def handle_my_sign1(self, name):

        if name not in Myclass.knowledge_graphs_class.keys():
            Myclass.knowledge_graphs_class[name] = {"entities": [], "relations": [], 'save_dir': Myclass.readfilepath,
                                                    'is_change': True}
            Myclass.current_kg_name = name
            self.update_kg_treeview()
            self.treeView_kg.setselect(name)

    def handle_my_sign2(self, name):
        if name not in Myclass.knowledge_graphs_class.keys():
            self.treeView_kg.copy_kg(Myclass.current_kg_name, name)
            self.update_kg_treeview()

    def deleteAll(self, thisLayout):
        if thisLayout is None:
            return
        item_list = list(range(thisLayout.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序

        for i in item_list:
            item = thisLayout.itemAt(i)
            thisLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
            else:
                self.deleteAll(item)

    # 03/21
    def add_entity(self, kg_name, entity_name, entity_type):
        if kg_name in self.knowledge_graphs:
            entity = {"name": entity_name, "type": entity_type}
            self.knowledge_graphs[kg_name]["entities"].append(entity)
            self.is_kg_changed = True
            print("is_kg_changed" + self.is_kg_changed)

    def add_relation(self, kg_name, head_entity_name, tail_entity_name, relation_type="包含关系"):
        if kg_name in self.knowledge_graphs and relation_type in Myclass.relationType_dict:
            # 确保实体存在
            entities = self.knowledge_graphs[kg_name]["entities"]
            head_entity = next((e for e in entities if e["name"] == head_entity_name), None)
            tail_entity = next((e for e in entities if e["name"] == tail_entity_name), None)
            if head_entity and tail_entity:  # 确保头尾实体都存在
                relation = (head_entity_name, tail_entity_name, relation_type)
                self.knowledge_graphs[kg_name]["relations"].append(relation)
                self.is_kg_changed = True
                print("is_kg_changed" + self.is_kg_changed)

    def remove_relation(self, kg_name, head_entity_name, tail_entity_name, relation_type):
        if kg_name in self.knowledge_graphs:
            # 找到并删除指定的关系
            relations = self.knowledge_graphs[kg_name]["relations"]
            self.knowledge_graphs[kg_name]["relations"] = [
                relation for relation in relations
                if not (relation[0] == head_entity_name and relation[1] == tail_entity_name and relation[
                    2] == relation_type)
            ]
            self.is_kg_changed = True
            print("is_kg_changed" + self.is_kg_changed)

    def remove_entity(self, kg_name, entity_name):
        if kg_name in self.knowledge_graphs:
            # 删除实体
            entities = self.knowledge_graphs[kg_name]["entities"]
            self.knowledge_graphs[kg_name]["entities"] = [
                entity for entity in entities if entity["name"] != entity_name
            ]

            # 删除与该实体有关的所有关系
            relations = self.knowledge_graphs[kg_name]["relations"]
            self.knowledge_graphs[kg_name]["relations"] = [
                relation for relation in relations
                if relation[0] != entity_name and relation[1] != entity_name
            ]
            print("is_kg_changed" + self.is_kg_changed)

    # 03/21 kg点击槽函数
    def on_kg_selected(self, selected, deselected):
        indexes = selected.indexes()
        self.graphicsView.remove_drag_link()
        if indexes:
            selected_index = indexes[0]
            # 检查是否选中的是第二层节点
            parent_index = selected_index.parent()
            if parent_index.isValid() and parent_index.parent().row() == -1:  # 确认是第二层节点
                Myclass.current_kg_name = selected_index.data()
                self.graphicsSence.update_kg()
                print("当前选中的知识图谱:", Myclass.current_kg_name)
            else:
                Myclass.current_kg_name = ''

    def update_treeview_with_new_entity(self, entity_name, type):
        model = self.treeView_kg.model()

        # 遍历模型来定位到知识图谱名对应的节点
        for i in range(model.rowCount()):
            for j in range(model.item(i).rowCount()):
                kg_item = model.item(i).child(j)  # 第二层节点，知识图谱名
                print("now finding kg" + current_kg_name)
                print(kg_item.text())
                if kg_item.text() == current_kg_name:

                    # 找到对应的知识图谱节点后，定位到实体列表
                    # 这里假设“实体列表”是知识图谱名下的第一个子节点
                    entities_list_item = kg_item.child(0)  # 实体列表节点
                    if entities_list_item:  # 确保实体列表节点存在
                        if type == 1:
                            # 创建并添加新实体节点
                            new_entity_item = QtGui.QStandardItem(entity_name)
                            entities_list_item.appendRow(new_entity_item)
                        if type == 2:
                            # 遍历第四层节点，找到并删除指定实体节点
                            for k in range(entities_list_item.rowCount()):
                                entity_item = entities_list_item.child(k)
                                if entity_item and entity_item.text() == entity_name:
                                    # 删除实体节点
                                    entities_list_item.removeRow(k)
                                    return
                    return

    def update_treeview_with_new_relation(self, head_entity, tail_entity, relation_type, type):
        model = self.treeView_kg.model()

        # 遍历模型来定位到知识图谱名对应的节点
        for i in range(model.rowCount()):
            for j in range(model.item(i).rowCount()):
                kg_item = model.item(i).child(j)  # 第二层节点，知识图谱名
                print("now finding kg" + current_kg_name)
                print(kg_item.text())
                if kg_item.text() == current_kg_name:
                    relations_list_item = kg_item.child(1)
                    if type == 1:
                        # 假设“关系列表”是知识图谱名下的第二个子节点
                        relation_name = f"{head_entity} - {relation_type} - {tail_entity}"
                        new_relation_item = QtGui.QStandardItem(relation_name)
                        relations_list_item.appendRow(new_relation_item)
                    if type == 2:
                        # 遍历第四层节点，找到并删除指定实体节点
                        for k in range(relations_list_item.rowCount()):
                            relation_item = relations_list_item.child(k)
                            relation_name = f"{head_entity} - {relation_type} - {tail_entity}"
                            if relation_item and relation_item.text() == relation_name:
                                # 删除实体节点
                                relations_list_item.removeRow(k)
                                return

    def onEntityDropped(self, entity_name):
        print("Dropped entity:", entity_name)
        entity_name = entity_name
        # 在这里实现添加实体到知识图谱和更新树视图的逻辑
        entity_type = self.now_entity_type

        # if entity_type in self.entityType_dict:

        self.add_entity(current_kg_name, entity_name, entity_type)

        self.update_treeview_with_new_entity(entity_name, 1)

    def onEntityRemoved(self, entity_name):
        print("Removed entity:", entity_name)
        entity_name = entity_name
        self.remove_entity(current_kg_name, entity_name)
        self.update_treeview_with_new_entity(entity_name, 2)

    def onRelationAdded(self, head_entity, tail_entity):
        self.add_relation(current_kg_name, head_entity, tail_entity)
        self.update_treeview_with_new_relation(head_entity, tail_entity, "包含关系", 1)

    def onRelationRemoved(self, head_entity, tail_entity):
        self.remove_relation(current_kg_name, head_entity, tail_entity, "包含关系")
        self.update_treeview_with_new_relation(head_entity, tail_entity, "包含关系", 2)


if __name__ == '__main__':
    # gc.enable()
    try:
        if not os.path.exists(r'./.picture'):
            os.makedirs(r'./.picture')
        gc.set_debug(gc.DEBUG_LEAK)
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        app = 0
        app = QtWidgets.QApplication(sys.argv)
        QtCore.QResource.registerResource('resources.qrc')
        MainWindow = my_MainWindow()
        # MainWindow = QCandyUi.CandyWindow.createWindow(MainWindow,'blue')

        desktop = QApplication.desktop()
        screen = app.primaryScreen()
        available_geometry = screen.availableGeometry()
        rect = desktop.frameSize()
        MainWindow.resize(QSize(available_geometry.width(), available_geometry.height()))
        # MainWindow.showFullScreen()
        # apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
        # MainWindow.showFullScreen()  # 显示主窗口
        MainWindow.show()
        # app.exec_()
        sys.exit(app.exec_())  # 在主线程中退出
    # 收集所有对象
#     all_objects = gc.get_objects()
#     # 打印对象数量
#     print(len(all_objects))
#
#     # 查找未被垃圾回收的对象
#     unreachable = []
#     for obj in all_objects:
#         if gc.get_referents(obj):
#             unreachable.append(obj)
#             print(obj)
#
#     # 打印未被垃圾回收的对象
# #        print(unreachable)
    except Exception as e:
        with open('error.txt','a',encoding='utf-8') as f:
            f.write(str(e)+"\n")

