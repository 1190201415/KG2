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
import sys
from xml import etree

from PyQt5 import QtCore, QtWidgets

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, Qt, QCoreApplication
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QGraphicsItem, QGraphicsPixmapItem, \
    QGraphicsEllipseItem, QAbstractItemView, QListView, QProgressDialog, QHBoxLayout, QVBoxLayout, QSplitter

import Myclass
from Myclass import current_kg_name
from untitled import Ui_MainWindow
from new_entity import Ui_Form
import xml.etree.ElementTree as ET
import pretty_xml


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

    def clickpushbutton_2(self):
        self.close()


class my_MainWindow(QMainWindow, Ui_MainWindow):
    knowledge_graphs = {
        "知识图谱1": {
            "entities": [],
            "relations": []
        },
    }
    num = 1

    def __init__(self, parent=None):
        super(my_MainWindow, self).__init__(parent)

        self.setWindowTitle('知识图谱编辑器')
        self.now_entity_type = None
        self.now_relation_type = None
        self.setupUi(self)

        self.initentityType()
        self.initrelationType()
        self.init_treeview(self.treeView, Myclass.entityType_dict, name='默认实体类型列表')
        # self.init_treeview(self.treeView_2, self.KG_dict, name='元知识图谱')
        # self.graphicsSence = Myclass.GraphicScene(parent=self.centralwidget)

        # 需要在class文件中修改这两句，很恶心（最好不要变动untitled。py，每次变都要改）
        # self.graphicsView = Myclass.GraphicView(parent=self.centralwidget, graphic_scene=self.graphicsSence)#
        # self.graphicsView.setGeometry(QtCore.QRect(225, 51, 661, 611))
        self.graphicsView.setObjectName("graphicsView")

        self.graphicsView.setSceneRect(0, 0, 10000, 10000)  # 设置场景大小
        self.treeView_kg.my_sign_kg.connect(self.update_kg_treeview)
        # self.graphicsView.entityDropped.connect(self.onEntityDropped)
        # self.graphicsSence.entityRemove.connect(self.onEntityRemoved)
        # self.graphicsView.relationAdded.connect(self.onRelationAdded)
        # self.graphicsView.relationRemove.connect(self.onRelationRemoved)

        self.init_treeview(self.treeView_3, Myclass.relationType_dict, name='默认关系类型列表')
        self.treeView.setDragEnabled(True)
        self.treeView_kg.setAcceptDrops(True)
        self.treeView.setDragDropMode(QListView.DragOnly)

        self.init_kg_treeview()
        self.treeView_kg.selectionModel().selectionChanged.connect(self.on_kg_selected)

        self.treeView.clicked.connect(self.clicked_treeView)
        self.treeView_3.clicked.connect(self.clicked_treeView3)
        self.action1_1.triggered.connect(self.clickaction1_1)

        # self.initLayouts()
        self.showMaximized()

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
        if text == '线型1':
            self.graphicsView.draw_link_flag = 1
            self.graphicsView.setCursor(Qt.DragLinkCursor)
        if text == '线型2':
            self.graphicsView.draw_link_flag = 2
            self.graphicsView.setCursor(Qt.DragLinkCursor)
        if text == '线型3':
            self.graphicsView.draw_link_flag = 3
            self.graphicsView.setCursor(Qt.DragLinkCursor)
        if text == '鼠标':
            self.graphicsView.draw_link_flag = 0
            if self.graphicsView.drag_link is not None:
                self.graphicsView.drag_link.remove()
                self.graphicsView.drag_link = None
            self.graphicsView.setCursor(Qt.ArrowCursor)

    def clicked_treeView(self):
        index = self.treeView.currentIndex()
        text = self.treeView.model().data(index)
        print(text)

    def init_treeview(self, treeView, dict, name=''):
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
        # 03/21：初始化右侧树视图

    def init_kg_treeview(self):
        # 创建模型
        self.model_kg = QtGui.QStandardItemModel()
        self.model_kg.setHorizontalHeaderLabels([''])
        self.treeView_kg.setModel(self.model_kg)

        # 添加数据示例
        root_item = QtGui.QStandardItem("元知识图谱")
        self.model_kg.appendRow(root_item)

        # 示例：添加几个知识图谱
        for i in range(1, 2):
            kg_item = QtGui.QStandardItem(f"知识图谱{i}")
            root_item.appendRow(kg_item)

            # # 为每个知识图谱添加实体和关系列表
            # entities_item = QtGui.QStandardItem("实体列表")
            # relations_item = QtGui.QStandardItem("关系列表")
            # kg_item.appendRow(entities_item)
            # kg_item.appendRow(relations_item)

            # 示例：为每个列表添加几个条目
            # for j in range(1, 3):
            #     entities_item.appendRow(QtGui.QStandardItem(f"实体{j}"))
            #     relations_item.appendRow(QtGui.QStandardItem(f"关系{j}"))

    def update_kg_treeview(self):
        for i in range(self.model_kg.rowCount()):
            for j in range(self.model_kg.item(i).rowCount()):
                self.model_kg.item(i).removeRow(j)
            self.model_kg.removeRow(i)
        # 添加数据示例
        root_item = QtGui.QStandardItem("元知识图谱")
        self.model_kg.appendRow(root_item)

        for i in Myclass.knowledge_graphs_class.keys():
            kg_item = QtGui.QStandardItem(i)
            root_item.appendRow(kg_item)

            # # 为每个知识图谱添加实体和关系列表
            # entities_item = QtGui.QStandardItem("实体列表")
            # relations_item = QtGui.QStandardItem("关系列表")
            # kg_item.appendRow(entities_item)
            # kg_item.appendRow(relations_item)

            # 示例：为每个列表添加几个条目
            # for j in range(1, 3):
            #     entities_item.appendRow(QtGui.QStandardItem(f"实体{j}"))
            #     relations_item.appendRow(QtGui.QStandardItem(f"关系{j}"))

    def click_kg_treeview_selected(self):
        # 获取当前选中的项
        index = self.treeView_kg.currentIndex()
        item = self.model_kg.itemFromIndex(index)
        self.graphicsSence.update_kg()
        print(f"当前选中的项：{item.text()}")
        # 在这里可以根据选中的项进行进一步的操作

    def closeEvent(self, a0: QtGui.QCloseEvent):
        NUM_FUN = 5
        self.progressDialog = QProgressDialog('保存进度', None, 0, NUM_FUN, self)
        self.progressDialog.setWindowTitle("退出中")
        self.progressDialog.setWindowFlags((self.progressDialog.windowFlags() & ~Qt.WindowCloseButtonHint))
        self.progressDialog.show()

        self.save_entityType()
        self.progressDialog.setValue(1)
        QCoreApplication.processEvents()

        self.save_relationType()
        self.progressDialog.setValue(2)
        QCoreApplication.processEvents()

        self.save_relationType()
        self.progressDialog.setValue(3)
        QCoreApplication.processEvents()

        self.save_kgs()
        self.progressDialog.setValue(NUM_FUN)
        a0.accept()

    def save_kg(self, name, kg):
        root = ET.Element('KG')
        entities = ET.SubElement(root, 'entities')
        relations = ET.SubElement(root, 'relations')
        for i in kg['entities']:
            print(i)
            entity = ET.SubElement(entities, 'entity')
            id = ET.SubElement(entity, 'id')
            name1 = ET.SubElement(entity, 'class_name')
            classification = ET.SubElement(entity, 'classification')
            identity = ET.SubElement(entity, 'identity')
            level = ET.SubElement(entity, 'level')
            attach = ET.SubElement(entity, 'attach')
            opentool = ET.SubElement(entity, 'opentool')
            content = ET.SubElement(entity, 'content')
            x = ET.SubElement(entity, 'x')
            y = ET.SubElement(entity, 'y')
            id.text = str(i.entity.id)
            name1.text = i.entity.class_name
            classification.text = i.entity.classification
            identity.text = i.entity.identity
            level.text = i.entity.level
            opentool.text = i.entity.opentool
            content.text = i.entity.content
            attach.text = i.entity.attach.tostring()
            x.text = str(i.entity.x)
            y.text = str(i.entity.y)
        for i in kg['relations']:
            relation = ET.SubElement(relations, 'relation')
            name2 = ET.SubElement(relation, 'name')
            headnodeid = ET.SubElement(relation, 'headnodeid')
            tailnodeid = ET.SubElement(relation, 'tailnodeid')
            class_name = ET.SubElement(relation, 'class_name')
            mask = ET.SubElement(relation, 'mask')
            classification = ET.SubElement(relation, 'classification')
            head_need = ET.SubElement(relation, 'head_need')
            tail_need = ET.SubElement(relation, 'tail_need')
            name2.text = i.relation.name
            headnodeid.text = str(i.relation.headnodeid)
            tailnodeid.text = str(i.relation.tailnodeid)
            class_name.text = i.relation.class_name
            mask.text = i.relation.mask
            classification.text = i.relation.classification
            head_need.text = i.relation.head_need
            tail_need.text = i.relation.tail_need
        tree = ET.ElementTree(root)
        tree.write(name + '.xml')
        pretty_xml.pretty(name=name + ".xml")

    def save_kgs(self):
        for KG in Myclass.knowledge_graphs_class.keys():
            self.save_kg(name=KG, kg=Myclass.knowledge_graphs_class[KG])

    def save_relationType(self):
        for relationType in Myclass.relationType_dict.keys():
            pass

    def save_entityType(self):
        for entityType in Myclass.entityType_dict.keys():
            pass

    def initrelationType(self):
        Myclass.relationType_dict["LineType1"] = Myclass.relationType(class_name='线型1', mask='知识连线',
                                                                      classification='包含关系',
                                                                      head_need='内容方法型节点', tail_need='内容方法型节点')
        Myclass.relationType_dict["LineType2"] = Myclass.relationType(class_name='线型2', mask='知识连线',
                                                                      classification='次序关系',
                                                                      head_need='内容方法型节点', tail_need='内容方法型节点')
        Myclass.relationType_dict["LineType3"] = Myclass.relationType(class_name='线型3', mask='知识—资源连线',
                                                                      classification='连接资源',
                                                                      head_need='内容方法型节点', tail_need='资源型节点')
        Myclass.relationType_dict["LineType4"] = Myclass.relationType(class_name='鼠标', mask='无',
                                                                      classification='无',
                                                                      head_need='无', tail_need='无')

    def initentityType(self):
        Myclass.entityType_dict["NodeType1"] = Myclass.entityType(class_name='知识领域节点', classification='内容方法型节点',
                                                                  identity='知识',
                                                                  level='一级', opentool='无')
        Myclass.entityType_dict["NodeType2"] = Myclass.entityType(class_name='知识单元节点', classification='内容方法型节点',
                                                                  identity='知识',
                                                                  level='二级', opentool='无')
        Myclass.entityType_dict["NodeType3"] = Myclass.entityType(class_name='知识点节点', classification='内容方法型节点',
                                                                  identity='知识',
                                                                  level='归纳级', opentool='无')
        Myclass.entityType_dict["NodeType4"] = Myclass.entityType(class_name='知识细节节点', classification='内容方法型节点',
                                                                  identity='知识',
                                                                  level='内容级', opentool='无')
        Myclass.entityType_dict["NodeType5"] = Myclass.entityType(class_name='视频型节点', classification='资源型节点',
                                                                  identity='Video',
                                                                  level='微课', opentool='Mvideo.exe')
        Myclass.entityType_dict["NodeType6"] = Myclass.entityType(class_name='测试题型节点', classification='资源型节点',
                                                                  identity='Exec',
                                                                  level='练习题', opentool='YUKETANG.exe')
        Myclass.entityType_dict["NodeType7"] = Myclass.entityType(class_name='文档型节点', classification='资源型节点',
                                                                  identity='PDF',
                                                                  level='教学素材', opentool='PDFviewer')

    def clickaction1_1(self):
        self.childwindow = childwindow_1()

        self.childwindow.my_sign1.connect(self.handle_my_sign1)

        self.childwindow.show()

    def insert_EntityType(self, name, class_name='默认实体类型列表'):
        model = self.treeView.model()
        for i in range(model.rowCount()):
            m_name = model.item(i).text()
            if m_name == class_name:
                model.item(i).appendRow(QtGui.QStandardItem(name))

    def handle_my_sign1(self, name):
        if name not in Myclass.knowledge_graphs_class.keys():
            Myclass.knowledge_graphs_class[name] = {"entities": [], "relations": []}
            self.update_kg_treeview()

    def deleteAll(self, thisLayout):
        if thisLayout == None:
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

    def add_relation(self, kg_name, head_entity_name, tail_entity_name, relation_type="线型1"):
        if kg_name in self.knowledge_graphs and relation_type in Myclass.relationType_dict:
            # 确保实体存在
            entities = self.knowledge_graphs[kg_name]["entities"]
            head_entity = next((e for e in entities if e["name"] == head_entity_name), None)
            tail_entity = next((e for e in entities if e["name"] == tail_entity_name), None)
            if head_entity and tail_entity:  # 确保头尾实体都存在
                relation = (head_entity_name, tail_entity_name, relation_type)
                self.knowledge_graphs[kg_name]["relations"].append(relation)

    def remove_relation(self, kg_name, head_entity_name, tail_entity_name, relation_type):
        if kg_name in self.knowledge_graphs:
            # 找到并删除指定的关系
            relations = self.knowledge_graphs[kg_name]["relations"]
            self.knowledge_graphs[kg_name]["relations"] = [
                relation for relation in relations
                if not (relation[0] == head_entity_name and relation[1] == tail_entity_name and relation[
                    2] == relation_type)
            ]

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

    # 03/21 kg点击槽函数
    def on_kg_selected(self, selected, deselected):
        indexes = selected.indexes()
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
        self.update_treeview_with_new_relation(head_entity, tail_entity, "线型1", 1)

    def onRelationRemoved(self, head_entity, tail_entity):
        self.remove_relation(current_kg_name, head_entity, tail_entity, "线型1")
        self.update_treeview_with_new_relation(head_entity, tail_entity, "线型1", 2)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 初始化界面
    MainWindow = my_MainWindow()
    MainWindow.show()  # 显示主窗口
    sys.exit(app.exec_())  # 在主线程中退出