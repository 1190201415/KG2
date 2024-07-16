# -*-coding = utf-8 -*-
# @Time : 2024/2/19 17:42
# @Author :skq
# @File : Myclass.py
# @Software: PyCharm
import copy
import math
import os
import typing
from pathlib import Path

import numpy as np
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsEllipseItem, \
    QGraphicsItem, QTreeView, QGraphicsPathItem, QGraphicsItemGroup, QGraphicsSimpleTextItem, QWidget, \
    QGraphicsTextItem, \
    QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent, QDialog, QInputDialog, QMenu, QAction, \
    QAbstractItemView, QMessageBox, QComboBox, QCheckBox
from PyQt5.QtCore import Qt, QPointF, QPoint, pyqtSignal, QRectF, QModelIndex, QSize
from PyQt5.QtGui import QColor, QPen, QPainter, QPixmap, QPainterPath, QBrush, QFont, QTransform, QPainterPathStroker, \
    QCursor, QImage, QWheelEvent
from typing import List, Dict

from entity2 import Ui_Dialog_2
from setitem import roll
import pretty_xml
from entity1 import Ui_Dialog
import xml.etree.ElementTree as ET


class meta_kg(object):
    def __init__(self):
        self.entityType_dict = {}
        self.ktsqepType_dict = {}
        self.relationType_dict = {}
        self.knowledge_graphs_class = {
            # "知识图谱1": {
            #     "entities": [],
            #     "relations": []
            # },
        }
        self.current_kg_name = '知识图谱1'
        self.node_id = 0
        self.save_dict = {}
        self.readfilepath = './xml'


meta_dict = {}
current_meta_kg_dict = '教学知识图谱'
readfilepath = './xml'


def init_meta_kg_dict():
    meta_dict['教学知识图谱'] = meta_kg()
    meta_dict['能力知识图谱'] = meta_kg()


entityType_dict = {}
ktsqepType_dict = {}
relationType_dict = {}
knowledge_graphs_class = {
    # "知识图谱1": {
    #     "entities": [],
    #     "relations": []
    # },
}
current_kg_name = '知识图谱1'
node_id = 0
save_dict = {}


def save_meta_kg():
    global entityType_dict, ktsqepType_dict, relationType_dict, knowledge_graphs_class, current_kg_name, node_id, readfilepath
    kg_dict: meta_kg
    kg_dict = meta_dict[current_meta_kg_dict]
    kg_dict.entityType_dict = entityType_dict
    kg_dict.ktsqepType_dict = ktsqepType_dict
    kg_dict.relationType_dict = relationType_dict
    kg_dict.knowledge_graphs_class = knowledge_graphs_class
    kg_dict.current_kg_name = current_kg_name
    kg_dict.node_id = node_id
    kg_dict.readfilepath = readfilepath
    kg_dict.save_dict = save_dict


def change_meta_kg():
    global entityType_dict, ktsqepType_dict, relationType_dict, knowledge_graphs_class, current_kg_name, node_id, save_dict, readfilepath
    kg_dict: meta_kg
    kg_dict = meta_dict[current_meta_kg_dict]
    entityType_dict = kg_dict.entityType_dict
    ktsqepType_dict = kg_dict.ktsqepType_dict
    relationType_dict = kg_dict.relationType_dict
    knowledge_graphs_class = kg_dict.knowledge_graphs_class
    current_kg_name = kg_dict.current_kg_name
    node_id = kg_dict.node_id
    readfilepath = kg_dict.readfilepath
    save_dict = kg_dict.save_dict


def other_save_kg(parent):
    name = current_kg_name
    kg = knowledge_graphs_class[name]
    isexist(name='temp')
    if name not in save_dict.keys():
        save_dict[name] = name
    text1, okPressed = QInputDialog.getText(parent, '另存为', "输入新名字", text=save_dict[name])
    if not (okPressed and text1 != ''):
        return
    save_dict[name] = text1
    print(save_dict)
    name = text1
    save_kg(name=name, kg=kg, dir=kg['save_dir'])


def save_kg(name, kg, dir=None):
    if dir is None:
        dir = './temp'
    if name in save_dict.keys():
        name = save_dict[name]
    isexist(name='temp')
    root = ET.Element('KG')
    root.text = current_meta_kg_dict
    entities = ET.SubElement(root, 'entities')
    relations = ET.SubElement(root, 'relations')
    for i in kg['entities']:
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
    print(dir)
    print(name)
    tree.write(os.path.join(dir, name) + '.xml')
    pretty_xml.pretty(name=os.path.join(dir, name) + ".xml")


def isexist(name, path=None):
    if path is None:
        path = os.getcwd()
    if os.path.exists(path + '/' + name):
        print("Under the path: " + path + '\n' + name + " is exist")
        return True
    else:
        if (os.path.exists(path)):
            os.makedirs(path + '/' + name)
            print("Under the path: " + path + '\n' + name + " is not exist")
        else:
            print("This path could not be found: " + path + '\n')
        return False


def save_kgs(dir=None):
    global knowledge_graphs_class
    for KG in knowledge_graphs_class.keys():
        print('保存kg：', KG)
        knowledge_graphs_class[KG]['save_dir'] = dir
        save_kg(name=KG, kg=knowledge_graphs_class[KG], dir=dir)


class abilityentityType(object):
    def __init__(self, class_name, EN):
        self.class_name = class_name
        self.EN = EN


class abilityrelationType(object):
    def __init__(self, class_name):
        self.class_name = class_name


class abilityentity(abilityentityType):
    def __init__(self, class_name, EN):
        super().__init__(class_name, EN)


class abilityrelation(abilityrelationType):
    def __init__(self, class_name):
        super().__init__(class_name)


class ABattachment(object):
    def __init__(self, L1=False, L2=False, L3=False, L4=False, L5=False, L6=False, L7=False, L8=False, L9=False,
                 Pj=False, Tk=False):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.L4 = L4
        self.L5 = L5
        self.L6 = L6
        self.L7 = L7
        self.L8 = L8
        self.L9 = L9
        self.Pj = Pj
        self.Tk = Tk

    def string(self):
        str1 = ''
        attri = vars(self)
        for a, v in attri.items():
            str1 = str1 + a
        return str1

    def tostring(self):
        str1 = ''
        # attri = vars(self)
        # for a, v in attri.items():
        #     if v:
        #         str1 = str1 + '1'
        #     else:
        #         str1 = str1 + '0'
        if self.L1:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.L2:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.L3:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.L4:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.L5:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.L6:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.L7:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.L8:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.L9:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.Pj:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.Tk:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        # self.T = self.tobool(str[0])
        # self.Z = self.tobool(str[1])
        # self.Q = self.tobool(str[2])
        # self.K = self.tobool(str[3])
        # self.E = self.tobool(str[4])
        # self.P = self.tobool(str[5])

        return str1

    def restrlist(self):
        list1 = []
        attri = vars(self)
        for a, v in attri.items():
            if v:
                list1.append(a)

        return list1

    def currentTrue(self):
        attri = vars(self)
        for a, v in attri.items():
            if v:
                return a
        return ''

    def restrlist2(self):
        list1 = []
        attri = vars(self)
        for a, v in attri.items():
            list1.append([v, a])
        return list1

    def tobool(self, str):
        if str == '0':
            return False
        if str == '1':
            return True

    def allfalse(self):
        attri = vars(self)
        for a, v in attri.items():
            setattr(self, a, False)

    def getbool(self, text):
        if hasattr(self, text):
            return getattr(self, text)

    def textto(self, text, f):
        self.allfalse()
        if hasattr(self, text):
            setattr(self, text, f)

    def stringTo(self, str):
        # attri = vars(self)
        # num = 0
        # for a, v in attri.items():
        #     setattr(self, a, self.tobool(str[num]))
        #     num = num + 1
        self.L1 = self.tobool(str[0])
        self.L2 = self.tobool(str[1])
        self.L3 = self.tobool(str[2])
        self.L4 = self.tobool(str[3])
        self.L5 = self.tobool(str[4])
        self.L6 = self.tobool(str[5])
        self.L7 = self.tobool(str[6])
        self.L8 = self.tobool(str[7])
        self.L9 = self.tobool(str[8])
        self.Pj = self.tobool(str[9])
        self.Tk = self.tobool(str[10])


class attachment(object):
    def __init__(self, K=False, T=False, Z=False, E=False, Q=False, P=False):
        # self.T = T
        # self.Z = Z
        # self.Q = Q
        # self.K = K
        # self.E = E
        # self.P = P
        self.K = K
        self.T = T
        self.E = E
        self.Q = Q
        self.Z = Z
        self.P = P

    def string(self):
        str1 = ''
        attri = vars(self)
        for a, v in attri.items():
            str1 = str1 + a
        return str1

    def tostring(self):
        str1 = ''
        # attri = vars(self)
        # for a, v in attri.items():
        #     if v:
        #         str1 = str1 + '1'
        #     else:
        #         str1 = str1 + '0'
        if self.T:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.Z:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.Q:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.K:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.E:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        if self.P:
            str1 = str1 + '1'
        else:
            str1 = str1 + '0'
        # self.T = self.tobool(str[0])
        # self.Z = self.tobool(str[1])
        # self.Q = self.tobool(str[2])
        # self.K = self.tobool(str[3])
        # self.E = self.tobool(str[4])
        # self.P = self.tobool(str[5])

        return str1

    def restrlist(self):
        list1 = []
        attri = vars(self)
        for a, v in attri.items():
            if v:
                list1.append(a)

        return list1

    def restrlist2(self):
        list1 = []
        attri = vars(self)
        for a, v in attri.items():
            list1.append([v, a])
        return list1

    def tobool(self, str):
        if str == '0':
            return False
        if str == '1':
            return True

    def stringTo(self, str):
        # attri = vars(self)
        # num = 0
        # for a, v in attri.items():
        #     setattr(self, a, self.tobool(str[num]))
        #     num = num + 1
        self.T = self.tobool(str[0])
        self.Z = self.tobool(str[1])
        self.Q = self.tobool(str[2])
        self.K = self.tobool(str[3])
        self.E = self.tobool(str[4])
        self.P = self.tobool(str[5])


class relationType(object):
    def __init__(self, class_name='包含关系', mask='知识连线', classification='包含关系', head_need='内容方法型节点', tail_need='内容方法型节点'):
        self.class_name = class_name
        self.mask = mask
        self.classification = classification
        self.head_need = head_need
        self.tail_need = tail_need


class GraphNode(object):
    def __init__(self, id: int):
        self.id = id
        self.parent_list: List[GraphNode] = []
        self.child_list: List[GraphNode] = []

    def get_parentnum(self):
        return len(self.parent_list)

    def get_childnum(self):
        return len(self.child_list)

    def appendchild(self, child: 'GraphNode'):
        if child not in self.child_list:
            self.child_list.append(child)
            child.parent_list.append(self)

    def removechild(self, child: 'GraphNode'):
        if child in self.child_list:
            self.child_list.remove(child)
            child.parent_list.remove(self)

    def removechildbyid(self, id: int):
        for i in self.child_list:
            if id == i.id:
                self.removechild(i)

    def get_child(self):
        return copy.copy(self.child_list)

    def ifgreen(self) -> bool:
        if len(self.child_list) > 0:
            for i in self.child_list:
                if len(i.parent_list):
                    return True
        return False


class Graph(object):
    def __init__(self, node_list: list):
        self.node_list: List[GraphNode] = []
        for i in node_list:
            a = GraphNode(i)
            self.node_list.append(a)

    def get_node(self, id: int):
        for i in self.node_list:
            if i.id == id:
                return i
        return None

    def get_node_list(self):
        return copy.copy(self.node_list)

    def set_link(self, list1: list):
        if len(list1) == 2:
            start = self.get_node(list1[0])
            end = self.get_node(list1[1])
            if start is not None and end is not None:
                start.appendchild(end)

    def set_Graph(self, link_lisT: list):
        for i in link_lisT:
            self.set_link(i)

    def get_minInNode(self):
        list2 = []
        if len(self.node_list) == 0:
            return list2
        min = self.node_list[0].get_parentnum()
        for i in self.node_list:
            if i.get_parentnum() < min:
                min = i.get_parentnum()
        for i in self.node_list:
            if i.get_parentnum() == min:
                list2.append(i)
        return list2, min


class relation(object):
    def __init__(self, name='包含', headnodeid=0, tailnodeid=1, class_name='包含关系', mask='知识连线',
                 classification='包含关系', head_need='内容方法型节点', tail_need='内容方法型节点'):
        self.name = name
        self.headnodeid = headnodeid
        self.tailnodeid = tailnodeid
        self.class_name = class_name
        self.mask = mask
        self.classification = classification
        self.head_need = head_need
        self.tail_need = tail_need


class entityType(object):
    def __init__(self, class_name='知识单元', classification='内容方法型', identity='知识', level='一级', opentool='无'):
        self.class_name = class_name
        self.classification = classification
        self.identity = identity
        self.level = level
        self.opentool = opentool


class entity(object):
    def __init__(self, attach: typing.Union[attachment, ABattachment], x: int, y: int, content='无', class_name='知识单元',
                 classification='内容方法型',
                 identity='知识',
                 level='二级', opentool='无'):
        global node_id
        self.content = content
        self.id = node_id
        node_id = node_id + 1
        self.class_name = class_name
        self.classification = classification
        self.identity = identity
        self.level = level
        self.attach = attach
        self.opentool = opentool
        self.x = x
        self.y = y

    def print_self(self):
        attri = vars(self)
        for a, v in attri.items():
            print(a, v)

    def copy_itself(self):
        return entity(attach=copy.deepcopy(self.attach), x=self.x, y=self.y, content=copy.deepcopy(self.content),
                      class_name=copy.deepcopy(self.class_name),
                      classification=copy.deepcopy(self.classification), identity=copy.deepcopy(self.identity),
                      level=copy.deepcopy(self.level),
                      opentool=copy.deepcopy(self.opentool))


class my_treeview(QTreeView):
    my_sign_kg = pyqtSignal()
    myreadfile = False

    def __init__(self, scence, parent=None, ):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.scence = scence
        self.expandAll()
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # 打开右键菜单的策略
        self.customContextMenuRequested.connect(self.treeWidgetItem_fun)  # 绑定事件

        # 定义treewidget中item右键界面

    def treeWidgetItem_fun(self, pos):
        selected_indexes = self.selectionModel().selectedIndexes()
        print(selected_indexes)
        self.groupBox_menu = QMenu(self)
        self.actionA = QAction(u'保存至图片', self)
        self.groupBox_menu.addAction(self.actionA)
        self.actionA.triggered.connect(lambda: self.actionAf(selected_indexes))
        self.groupBox_menu.show()
        self.groupBox_menu.popup(QCursor.pos())

    def actionAf(self, listitem):
        reply = QMessageBox.question(self, 'Message', '确定删除？',
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for i in listitem:
                print(self.model().data(i))

    def initxml(self, path=None):
        if path is None:
            cwd = os.getcwd()
            path = os.path.join(cwd, 'xml')
        xmllist = os.listdir(path)
        for i in xmllist:
            i = os.path.join(path, i)
            self.readfile(path=i)
        return path

    def readfile(self, path=''):
        self.myreadfile = True
        global current_kg_name
        try:
            filePath = path
            dirname, full_name = os.path.split(filePath)
            filname, file_ext = os.path.splitext(full_name)
            if file_ext != '.xml':
                print('不是xml文件')
                return
            tree = ET.parse(filePath)  # 解析movies.xml这个文件
            filePath = Path(filePath)
            root = tree.getroot()  # 得到根元素，Element类
            meta_kg_name = root.text
            print('名字是', (meta_kg_name))
            if meta_kg_name is None or meta_kg_name == '\n\t':
                print('老旧xml')
                meta_kg_name = '教学知识图谱'
            if meta_kg_name.replace('\n\t', '') != current_meta_kg_dict:
                print(meta_kg_name, current_meta_kg_dict)
                return
            entities = root.findall('entities')
            relations = root.findall('relations')
            entitys = entities[0].findall('entity')
            now_kg_name = os.path.basename(filePath).split('.')[0]
        except Exception as e:
            print(e)
            print('xml文件有误,文件名：', path)
            return
        knowledge_graphs_class[now_kg_name] = {"entities": [], "relations": [], 'save_dir': dirname,
                                               'is_change': False}  # 直接覆盖掉之前的图谱
        relations1 = relations[0].findall('relation')
        idlist = []
        if current_meta_kg_dict == '教学知识图谱':
            for i in entitys:
                entity1 = entity(x=0, y=0, attach=attachment())
                for j in i:
                    if hasattr(entity1, j.tag):
                        if j.tag == 'attach':
                            entity1.attach.stringTo(j.text)
                            continue
                        if j.tag == 'x' or j.tag == 'y' or j.tag == 'id':
                            setattr(entity1, j.tag, int(float(j.text)))
                            continue
                        setattr(entity1, j.tag, j.text)
                if entity1.id in idlist:
                    continue
                idlist.append(entity1.id)
                itemgroup = GraphicItemGroup(scene=self.scence, entity=entity1, x=entity1.x, y=entity1.y)
                knowledge_graphs_class[now_kg_name]['entities'].append(itemgroup)
        elif current_meta_kg_dict == '能力知识图谱':
            for i in entitys:
                entity1 = entity(x=0, y=0, attach=ABattachment())
                for j in i:
                    if hasattr(entity1, j.tag):
                        if j.tag == 'attach':
                            print('attach_adsd',j.text)
                            entity1.attach.stringTo(j.text)
                            continue
                        if j.tag == 'x' or j.tag == 'y' or j.tag == 'id':
                            setattr(entity1, j.tag, int(float(j.text)))
                            continue
                        setattr(entity1, j.tag, j.text)
                if entity1.id in idlist:
                    continue
                idlist.append(entity1.id)
                itemgroup = ABGraphicItemGroup(scene=self.scence, entity=entity1, x=entity1.x, y=entity1.y)
                knowledge_graphs_class[now_kg_name]['entities'].append(itemgroup)
        for i in relations1:
            relation1 = relation()
            for j in i:
                if hasattr(relation1, j.tag):
                    setattr(relation1, j.tag, j.text)
            if int(relation1.headnodeid) == int(relation1.tailnodeid):
                continue
            itemrelation = Link(scene=self.scence, start_item=self.find_item(now_kg_name, int(relation1.headnodeid)),
                                end_item=self.find_item(now_kg_name, int(relation1.tailnodeid)),
                                flag=self.class_nameToflag(relation1.class_name))
            itemrelation.flagToentity()
            knowledge_graphs_class[now_kg_name]['relations'].append(itemrelation)
        knowledge_graphs_class[now_kg_name]['save_dir'] = dirname
        knowledge_graphs_class[now_kg_name]['is_change'] = False
        current_kg_name = now_kg_name
        self.scence.update_kg()
        self.my_sign_kg.emit()
        self.setselect(current_kg_name)
        self.expandAll()
        self.myreadfile = False

    def setselect(self, name):
        index = self.findIndexByText(self.model(), name)
        if index.isValid():
            print('设置成功')
            self.setCurrentIndex(index)
            self.selectionModel().select(index, self.selectionModel().Select)

    def findIndexByText(self, model, text):
        def search_item(item):
            for row in range(item.rowCount()):
                child = item.child(row)
                if child.text() == text:
                    return model.indexFromItem(child)
                if child.hasChildren():
                    index = search_item(child)
                    if index.isValid():
                        return index
            return QModelIndex()

        root_item = model.invisibleRootItem()
        return search_item(root_item)

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent):
        if e.mimeData().hasText():
            e.acceptProposedAction()
        else:
            e.ignore()

    def copy_kg(self, name1, name2):
        global current_kg_name
        current_kg_name = name2
        knowledge_graphs_class[name2] = {"entities": [], "relations": [], 'is_change': True}
        entities = knowledge_graphs_class[name1]['entities']
        relations = knowledge_graphs_class[name1]['relations']
        for i in entities:
            entity1 = copy.deepcopy(i.entity)
            entity = GraphicItemGroup(scene=self.scence, entity=entity1, x=entity1.x, y=entity1.y)
            knowledge_graphs_class[name2]['entities'].append(entity)
        for i in relations:
            relation1 = i.relation
            itemrelation = Link(scene=self.scence, start_item=self.find_item(name2, int(relation1.headnodeid)),
                                end_item=self.find_item(name2, int(relation1.tailnodeid)),
                                flag=self.class_nameToflag(relation1.class_name))
            itemrelation.flagToentity()
            knowledge_graphs_class[name2]['relations'].append(itemrelation)
        knowledge_graphs_class[name2]['save_dir'] = knowledge_graphs_class[name1]['save_dir']
        self.scence.update_kg()
        # self.my_sign_kg.emit()
        self.expandAll()

    def dragMoveEvent(self, event: QtGui.QMouseEvent):
        event.accept()

    def find_item(self, name, id):
        entities = knowledge_graphs_class[name]['entities']
        for i in entities:
            if id == i.entity.id:
                return i

    def class_nameToflag(self, class_name):
        dict1 = {'包含关系': 1, '次序关系': 2, '连接资源': 3, '关键次序': 4,'样式一':5,'样式二':6}

        return dict1[class_name]

    def dropEvent(self, e: QtGui.QDropEvent):
        global current_kg_name
        e.acceptProposedAction()
        filePathList = e.mimeData().text()
        filePath = filePathList.split('\n')[0]  # 拖拽多文件只取第一个地址
        filePath = filePath.replace('file:///', '', 1)  # 去除文件地址前缀的特定字符
        self.readfile(path=filePath)
        # tree = ET.parse(filePath)  # 解析movies.xml这个文件
        # filePath = Path(filePath)
        # root = tree.getroot()  # 得到根元素，Element类
        # entities = root.findall('entities')
        # relations = root.findall('relations')
        # entitys = entities[0].findall('entity')
        # meta_kg_name = root.text
        # if meta_kg_name is None or meta_kg_name == '\n\t':
        #     print('老旧xml')
        #     meta_kg_name = '教学知识图谱'
        # if meta_kg_name.replace('\n\t', '') != current_meta_kg_dict:
        #     print(meta_kg_name, current_meta_kg_dict)
        #     print('a' + meta_kg_name)
        #     print('b' + current_meta_kg_dict)
        #     return
        # now_kg_name = os.path.basename(filePath).split('.')[0]
        # if now_kg_name not in knowledge_graphs_class.keys():
        #     knowledge_graphs_class[now_kg_name] = {"entities": [], "relations": []}
        # if now_kg_name in knowledge_graphs_class.keys():
        #     knowledge_graphs_class[now_kg_name]['entities'].clear()
        #     knowledge_graphs_class[now_kg_name]['relations'].clear()
        # relations1 = relations[0].findall('relation')
        # for i in entitys:
        #     entity1 = entity(x=0, y=0, attach=attachment())
        #     for j in i:
        #         if hasattr(entity1, j.tag):
        #             if j.tag == 'attach':
        #                 entity1.attach.stringTo(j.text)
        #                 continue
        #             if j.tag == 'x' or j.tag == 'y' or j.tag == 'id':
        #                 setattr(entity1, j.tag, int(float(j.text)))
        #                 continue
        #             setattr(entity1, j.tag, j.text)
        #     itemgroup = GraphicItemGroup(scene=self.scence, entity=entity1, x=entity1.x, y=entity1.y)
        #     knowledge_graphs_class[now_kg_name]['entities'].append(itemgroup)
        # for i in relations1:
        #     relation1 = relation()
        #     for j in i:
        #         if hasattr(relation1, j.tag):
        #             setattr(relation1, j.tag, j.text)
        #     itemrelation = Link(scene=self.scence, start_item=self.find_item(now_kg_name, int(relation1.headnodeid)),
        #                         end_item=self.find_item(now_kg_name, int(relation1.tailnodeid)),
        #                         flag=self.class_nameToflag(relation1.class_name))
        #     itemrelation.flagToentity()
        #     knowledge_graphs_class[now_kg_name]['relations'].append(itemrelation)
        # current_kg_name = now_kg_name
        # self.scence.update_kg()
        # self.my_sign_kg.emit()
        # self.expandAll()


class my_Ui_Dialog(QDialog, Ui_Dialog):
    my_sign1 = pyqtSignal(entity)

    def __init__(self, parent=None, linetext='', content='', attach=attachment(), id=0, class_type=1):
        super(my_Ui_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.label_4.setText(str(id))
        self.setcombox(class_type=class_type)
        self.comboBox.setCurrentText(linetext)
        self.textEdit.setText(content)
        self.checkBox.setChecked(attach.K)
        self.checkBox_2.setChecked(attach.T)
        self.checkBox_3.setChecked(attach.Z)
        self.checkBox_4.setChecked(attach.E)
        self.checkBox_5.setChecked(attach.Q)
        self.checkBox_6.setChecked(attach.P)
        self.class_type = class_type
        self.pushButton_2.clicked.connect(self.clickpushbutton_2)
        self.setWindowFlags(Qt.Popup)
        self.show()
        self.activateWindow()

    def setcombox(self, class_type):
        list = []
        if class_type == 1:
            for i in entityType_dict.keys():
                if entityType_dict[i].classification == '内容方法型节点':
                    list.append(entityType_dict[i].class_name)
        elif class_type == 2:
            for i in entityType_dict.keys():
                if entityType_dict[i].classification == '资源型节点':
                    list.append(entityType_dict[i].class_name)
        self.comboBox.addItems(list)

    def setfEnable(self, flag: bool):
        self.checkBox.setEnabled(flag)
        self.checkBox_2.setEnabled(flag)
        self.checkBox_3.setEnabled(flag)
        self.checkBox_4.setEnabled(flag)
        self.checkBox_5.setEnabled(flag)
        self.checkBox_6.setEnabled(flag)

    def clickpushbutton(self):
        name = self.comboBox.currentText()
        content = self.textEdit.toPlainText()
        K_flag = self.checkBox.isChecked()
        T_flag = self.checkBox_2.isChecked()
        Z_flag = self.checkBox_3.isChecked()
        E_flag = self.checkBox_4.isChecked()
        Q_flag = self.checkBox_5.isChecked()
        P_flag = self.checkBox_6.isChecked()
        entity1 = entity(class_name=name, content=content, x=0, y=0,
                         attach=attachment(T=T_flag, Z=Z_flag, Q=Q_flag, K=K_flag, E=E_flag, P=P_flag))
        self.my_sign1.emit(entity1)
        self.close()

    def clickpushbutton_2(self):
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.clickpushbutton()
        a0.accept()


class ABmy_Ui_Dialog(QDialog, Ui_Dialog_2):
    my_sign1 = pyqtSignal(entity)

    def __init__(self, parent=None, linetext='', content='', attach=ABattachment(), id=0, class_type=1):
        super(ABmy_Ui_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.label_4.setText(str(id))
        self.check_boxes = []
        self.setcombox(class_type=1)
        self.comboBox.setCurrentText(linetext)
        self.textEdit.setText(content)
        # self.check_boxes.append(self.checkBox)
        # self.check_boxes.append(self.checkBox_2)
        # self.check_boxes.append(self.checkBox_3)
        # self.check_boxes.append(self.checkBox_4)
        # self.check_boxes.append(self.checkBox_5)
        # self.check_boxes.append(self.checkBox_6)
        self.class_type = class_type
        self.pushButton_2.clicked.connect(self.clickpushbutton_2)
        self.setcombox_2()
        self.comboBox_2.setCurrentText(attach.currentTrue())
        self.comboBox.currentIndexChanged.connect(self.setcombox_2)

        self.setWindowFlags(Qt.Popup)
        self.show()
        self.activateWindow()

    # def deletecheckbox(self):
    #     for i in self.check_boxes:
    #         self.gridLayout.removeWidget(i)
    #         i.setParent(None)
    #         i.deleteLater()  # 标记小部件供垃圾回收
    #
    #
    # def newcheckbox(self,list1):
    #     _translate = QtCore.QCoreApplication.translate
    #     self.check_boxes = []
    #     for v,a in list1:
    #         checkbo = QCheckBox(self)
    #         checkbo_name = a
    #         checkbo.setObjectName(checkbo_name)
    #         checkbo.setText(_translate("Dialog", a))
    #         checkbo.setChecked(v)
    #         self.gridLayout.addWidget(checkbo)
    #         self.check_boxes.append(checkbo)

    def setcombox(self, class_type):
        list = []
        if class_type == 1:
            for i in entityType_dict.keys():
                if entityType_dict[i].classification == '内容方法型节点':
                    list.append(entityType_dict[i].class_name)
        elif class_type == 2:
            for i in entityType_dict.keys():
                if entityType_dict[i].classification == '资源型节点':
                    list.append(entityType_dict[i].class_name)
        self.comboBox.addItems(list)

    def setcombox_2(self):
        self.comboBox_2.clear()
        list = []
        list.append('')
        linetext  = self.comboBox.currentText()
        if linetext == '能力点':
            for i in ktsqepType_dict.keys():
                if ktsqepType_dict[i].identity == '能力点':
                    list.append(ktsqepType_dict[i].class_name)
        elif linetext == '学生任务':
            for i in ktsqepType_dict.keys():
                if ktsqepType_dict[i].identity == '学生任务':
                    list.append(ktsqepType_dict[i].class_name)
        self.comboBox_2.addItems(list)

    def setfEnable(self, flag: bool):
        for i in self.check_boxes:
            i.setEnabled(flag)

    def clickpushbutton(self):
        name = self.comboBox.currentText()
        content = self.textEdit.toPlainText()
        flag = self.comboBox_2.currentText()
        a = ABattachment()
        if name == '能力点' and 'L' in flag:
            a.textto(flag,True)
        if name == '学生任务' and flag in ['Pj','Tk']:
            a.textto(flag,True)
        entity1 = entity(class_name=name, content=content, x=0, y=0,
                         attach=a)
        self.my_sign1.emit(entity1)
        self.close()

    def clickpushbutton_2(self):
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.clickpushbutton()
        a0.accept()


class GraphicScene(QGraphicsScene):
    entityRemove = pyqtSignal(str)
    scenechanged = pyqtSignal(bool)
    is_kg_changed = False

    def __init__(self, parent=None, ):
        super().__init__(parent)
        self.nodes = []
        self.links = []
        # 一些关于网格背景的设置
        # self.grid_size = 20  # 一块网格的大小 （正方形的）
        # self.grid_squares = 5  # 网格中正方形的区域个数

        # 一些颜色
        self._color_background = QColor(255, 255, 255)
        self._color_light = QColor(255, 255, 255)
        self._color_dark = QColor(255, 255, 255)
        # 一些画笔
        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        # 设置画背景的画笔
        self.setBackgroundBrush(self._color_background)
        self.setSceneRect(0, 0, 500, 500)
        self.is_kg_changed = False

    def P_deep_search(self, start_node: GraphNode, notgetlist: list, deep: float, length: float,
                      id_dict: Dict[int, typing.Union['GraphicItemGroup', 'ABGraphicItemGroup']]):
        node = id_dict[start_node.id]
        deep1 = deep + node.boundingRect().height() + 80
        node.setcentpos(length, deep)
        # node.setPos(length + 0.5 * node.boundingRect().width(), deep - 0.5 * node.boundingRect().height())
        # print(start_node.id, deep+0.5*node.boundingRect().height(),length + 0.5*node.boundingRect().width())
        for i in start_node.child_list:
            if i in notgetlist:
                notgetlist.remove(i)
                deep = self.P_deep_search(start_node=i, notgetlist=notgetlist, deep=deep,
                                          length=length + node.boundingRect().width() + 20, id_dict=id_dict)
        if deep1 > deep:
            return deep1
        else:
            return deep

    def AF_deep_search(self, start_node: GraphNode, notgetlist: list, deep: float, length: float,
                       id_dict: Dict[int, typing.Union['GraphicItemGroup', 'ABGraphicItemGroup']]):

        node = id_dict[start_node.id]
        deep1 = deep + node.boundingRect().height() + 80
        # print(start_node.id, deep+0.5*node.boundingRect().height(),length + 0.5*node.boundingRect().width())
        node_deep = deep
        list_child_deep = []
        for i in start_node.child_list:
            if i in notgetlist:
                notgetlist.remove(i)
                list_child_deep.append(deep)
                deep = self.AF_deep_search(start_node=i, notgetlist=notgetlist, deep=deep,
                                           length=length + node.boundingRect().width() + 40, id_dict=id_dict)
                # list_child_deep.append(deep)

        # if len(list_child_deep) >= 1:#使用实际在的位置进行平均
        #     all_deep = 0
        #     for i in start_node.child_list:
        #         all_deep = all_deep + id_dict[i.id].pos().y()
        #     node_deep = all_deep / len(list_child_deep)

        if len(list_child_deep) >= 1:  # 使用理论上在的位置进行平均
            all_deep = 0
            for i in list_child_deep:
                all_deep = all_deep + i
            node_deep = all_deep / len(list_child_deep)

        # if len(start_node.child_list) >= 1:
        #     all_deep = 0
        #     for i in start_node.child_list:
        #         all_deep = all_deep + id_dict[i.id].pos().y() - id_dict[i.id].boundingRect().height()*0.5
        #     node_deep = all_deep / len(start_node.child_list)

        node.setcentpos(length + 0.5 * node.boundingRect().width(), node_deep)
        #        if start_node.

        if deep1 > deep:
            return deep1
        else:
            return deep

    def auto_layout(self, point):
        global node_id
        isexist(name='.produrce')
        if current_kg_name not in knowledge_graphs_class.keys():
            return
        save_kg(current_kg_name, knowledge_graphs_class[current_kg_name],
                dir='./.produrce')
        self.deleall()
        self.clear()
        self.update()
        ax = 0
        entities = knowledge_graphs_class[current_kg_name]['entities']
        relations = knowledge_graphs_class[current_kg_name]['relations']
        id_dict = {}
        node_list = []
        rela_list = []
        fnode_list = []
        frela_list = []
        for i in entities:
            i: typing.Union['GraphicItemGroup', 'ABGraphicItemGroup']
            id_dict[i.entity.id] = i
            if i.entity.classification =='资源型节点':
                fnode_list.append(i.entity.id)
            else:
                node_list.append(i.entity.id)
        for j in relations:
            j: Link
            if j.start_item.entity.id in node_list and j.end_item.entity.id in node_list:
                rela_list.append([j.start_item.entity.id, j.end_item.entity.id])
            else:
                frela_list.append([j.start_item.entity.id, j.end_item.entity.id])

        graph = Graph(node_list=node_list)
        graph.set_Graph(rela_list)

        start_list, min = graph.get_minInNode()
        print('最小入度', min)
        deep = point.y()
        for k in start_list:
            deep = self.AF_deep_search(start_node=k, deep=deep, length=point.x(), notgetlist=graph.get_node_list(),
                                       id_dict=id_dict)

        for i in frela_list:
            if i[0] in node_list and i[1] in fnode_list:
                id_dict[i[1]].setcentpos(x=id_dict[i[0]].pos().x(),y=id_dict[i[0]].pos().y()+30)
                fnode_list.remove(i[1])

        for i in fnode_list:
            entities.remove(id_dict[i])

        for i in entities:
            if i.entity.id > ax:
                ax = i.entity.id
            self.nodes.append(i)
            self.addItem(i)
        for j in relations:
            self.links.append(j.gr_edge)
            self.addItem(j.gr_edge)
            j.update_positions()
        node_id = ax + 1
        self.update()
        save_kg(current_kg_name, knowledge_graphs_class[current_kg_name],
                dir='./temp')

    def deleall(self):
        for i in self.nodes:
            self.removeItem(i)
        self.nodes.clear()
        for i in self.links:
            self.removeItem(i)
        self.links.clear()

    def update_kg(self):
        global node_id
        self.deleall()
        self.clear()
        self.update()
        ax = 0
        if current_kg_name not in knowledge_graphs_class.keys():
            return
        entities = knowledge_graphs_class[current_kg_name]['entities']
        relations = knowledge_graphs_class[current_kg_name]['relations']
        for i in entities:
            if i.entity.id > ax:
                ax = i.entity.id
            self.nodes.append(i)
            self.addItem(i)
        for i in relations:
            self.links.append(i.gr_edge)
            self.addItem(i.gr_edge)
        node_id = ax + 1

    def update_links(self):
        for i in self.links:
            i.edge.update_positions()

    def add_node(self, node):
        if node not in self.nodes:
            # self.mainwindow.entity_dict.a
            self.nodes.append(node)
            self.addItem(node)
            knowledge_graphs_class[current_kg_name]['entities'].append(node)
            save_kg(name=current_kg_name, kg=knowledge_graphs_class[current_kg_name],
                    dir='./temp')
            self.is_kg_changed = True

    def add_link(self, link):
        if link not in self.links:
            self.links.append(link)
            self.addItem(link)
            knowledge_graphs_class[current_kg_name]['relations'].append(link.edge)
            self.is_kg_changed = True

    def remove_node(self, node):
        for i in range(len(self.links) - 1, -1,
                       -1):  # 倒序循环，从最后一个元素循环到第一个元素。不能用正序循环，因为正序循环删除元素后，后续的列表的长度和元素下标同时也跟着变了，由于len(alist)是动态的。
            if self.links[i].edge.start_item == node or self.links[i].edge.end_item == node:
                self.remove_link(self.links[i])
        if node not in self.nodes:
            return
        self.nodes.remove(node)
        self.removeItem(node)
        self.entityRemove.emit(node.name)
        knowledge_graphs_class[current_kg_name]['entities'].remove(node)
        del node
        # node.deleteLater()
        save_kg(name=current_kg_name, kg=knowledge_graphs_class[current_kg_name],
                dir='./temp')
        self.is_kg_changed = True

    def remove_link(self, link):
        print("删除", link)
        if link in self.links:
            self.links.remove(link)
            self.removeItem(link)
            knowledge_graphs_class[current_kg_name]['relations'].remove(link.edge)
            del link
            # link.deleteLater()
            save_kg(name=current_kg_name, kg=knowledge_graphs_class[current_kg_name],
                    dir='./temp')
            self.is_kg_changed = True

    def get_all_item(self):
        for item in self.nodes:
            print(item.give_pos())

    # override
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # # 获取背景矩形的上下左右的长度，分别向上或向下取整数
        # left = int(math.floor(rect.left()))
        # right = int(math.ceil(rect.right()))
        # top = int(math.floor(rect.top()))
        # bottom = int(math.ceil(rect.bottom()))
        #
        # # 从左边和上边开始
        # first_left = left - (left % self.grid_size)  # 减去余数，保证可以被网格大小整除
        # first_top = top - (top % self.grid_size)
        #
        # # 分别收集明、暗线
        # lines_light, lines_dark = [], []
        # for x in range(first_left, right, self.grid_size):
        #     if x % (self.grid_size * self.grid_squares) != 0:
        #         lines_light.append(QLine(x, top, x, bottom))
        #     else:
        #         lines_dark.append(QLine(x, top, x, bottom))
        #
        # for y in range(first_top, bottom, self.grid_size):
        #     if y % (self.grid_size * self.grid_squares) != 0:
        #         lines_light.append(QLine(left, y, right, y))
        #     else:
        #         lines_dark.append(QLine(left, y, right, y))
        #
        #     # 最后把收集的明、暗线分别画出来
        # painter.setPen(self._pen_light)
        # if lines_light:
        #     painter.drawLines(*lines_light)
        #
        # painter.setPen(self._pen_dark)
        # if lines_dark:
        #     painter.drawLines(*lines_dark)


class GraphicView(QGraphicsView):
    entityDropped = pyqtSignal(str)  # 假设信号传递实体名称和坐标
    relationAdded = pyqtSignal(str, str)
    relationRemove = pyqtSignal(str, str)
    move = pyqtSignal(bool)
    updateRequest = pyqtSignal()
    list_of_copy = []

    def __init__(self, graphic_scene: GraphicScene, parent=None):
        super().__init__(parent)
        self.gr_scene = graphic_scene  # 将scene传入此处托管，方便在view中维护
        self.parent = parent

        # 03/23
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)  # 设置拖拽模式为“手形”
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.drag_link: typing.Optional[Link] = None  # 记录拖拽时的线
        self.draw_link_flag = 0
        self.drag_flag = 0

        self.init_ui()

        self.startItem = None  # 拖拽开始的项（头结点）
        self.endItem = None  # 拖拽结束的项（尾结点）
        self.currentRelationType = None  # 当前关系类型，需要有途径设置

        # 03/23 用于拖拽的变量
        self.dragging = False
        self.lastMousePosition = None
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.create_rightmenu)

        self._zoom = 0
        self._maxZoom = 5
        self._minZoom = -5

    def init_ui(self):
        self.setScene(self.gr_scene)
        # 设置渲染属性
        self.setRenderHints(QPainter.Antialiasing |  # 抗锯齿
                            QPainter.HighQualityAntialiasing |  # 高品质抗锯齿
                            QPainter.TextAntialiasing |  # 文字抗锯齿
                            QPainter.SmoothPixmapTransform |  # 使图元变换更加平滑
                            QPainter.LosslessImageRendering)  # 不失真的图片渲染
        # 视窗更新模式
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # 设置水平和竖直方向的滚动条不显示
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBar(roll.setroll())
        self.setVerticalScrollBar(roll.setroll())
        self.setTransformationAnchor(self.AnchorUnderMouse)
        # 设置拖拽模式
        self.setDragMode(self.RubberBandDrag)
        self.setAcceptDrops(True)

    def save_as_picture(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as e:
                QMessageBox.critical(self, "错误", f"无法创建文件夹: {e}")
                return
        items_rect = self.gr_scene.itemsBoundingRect()
        base_file_path = os.path.join(path, current_kg_name + ".png")
        file_path = base_file_path
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(path, current_kg_name + f"_{counter}.png")
            counter += 1

        # 扩展尺寸（例如，增加20像素的边界）

        border_size = (items_rect.size().toSize().height() + items_rect.size().toSize().height()) * 0.2

        # 计算扩展后的尺寸
        expanded_size = items_rect.size().toSize() + QSize(border_size * 2, border_size * 2)

        # 创建一个新的QImage，尺寸扩大后的
        image = QImage(expanded_size, QImage.Format_ARGB32)
        image.fill(Qt.white)  # 设置背景为白色

        # 使用QPainter将场景绘制到QImage上
        painter = QPainter(image)

        # 目标矩形为扩大后的QImage尺寸，中间留出边界
        target_rect = QRectF(border_size, border_size, items_rect.width(), items_rect.height())

        # 使用QPainter将场景绘制到QImage上
        self.gr_scene.render(painter, target=target_rect, source=items_rect)

        painter.end()  # 结束绘制

        # 保存QImage到文件
        image.save(file_path)

    # 03/23
    def wheelEvent(self, event):
        zoomInFactor = 1.25  # 定义放大的比例因子
        zoomOutFactor = 1 / zoomInFactor  # 定义缩小的比例因子

        # 设置缩放的中心点为当前鼠标位置
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        # 滚轮向上滚动，放大
        if event.angleDelta().y() > 0:
            if self._zoom < self._maxZoom:
                self._zoom += 1
                self.scale(zoomInFactor, zoomInFactor)
            else:
                return
        # 滚轮向下滚动，缩小
        else:
            if self._zoom > self._minZoom:
                self._zoom -= 1
                self.scale(zoomOutFactor, zoomOutFactor)
            else:
                return

        event.accept()

    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        # current_item = self.parent.itemAt(pos)  # 获取当前坐标下的item
        # current_index = self.parent.indexFromItem(current_item)  # 获取该item的index
        # print(current_index)

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def get_view_left_middle(self):
        # 获取视口矩形
        rect = self.viewport().rect()
        # 获取视口左中点
        left_middle_point = rect.center()
        left_middle_point.setX(rect.left() + 0.1 * (rect.width()))
        left_middle_point.setY(rect.top() + 0.1 * (rect.height()))
        # 将视口左中点映射到场景坐标
        left_middle_scene_point = self.mapToScene(left_middle_point)
        return left_middle_scene_point

    def get_view_top_left(self):
        # 获取视口左上角点
        top_left_point = self.viewport().rect().topLeft()
        # 将视口左上角点映射到场景坐标
        top_left_scene_point = self.mapToScene(top_left_point)
        return top_left_scene_point

    def get_view_center(self):
        # 获取视口矩形
        rect = self.viewport().rect()
        # 获取视口中心点
        center_point = rect.center()
        # 将视口中心点映射到场景坐标
        center_scene_point = self.mapToScene(center_point)
        return center_scene_point

    def dragLeaveEvent(self, event):
        event.accept()
        # current_item = self.parent.itemAt(pos)  # 获取当前坐标下的item
        # current_index = self.parent.indexFromItem(current_item)  # 获取该item的index
        # print(current_index)

    def nameToentity(self, name, x, y):
        for i in entityType_dict.keys():
            j = entityType_dict[i]
            if name == j.class_name:
                if current_meta_kg_dict == '教学知识图谱':
                    return entity(class_name=j.class_name, classification=j.classification, identity=j.identity,
                                  level=j.level, opentool=j.opentool, attach=attachment(), x=x, y=y)
                elif current_meta_kg_dict == '能力知识图谱':
                    return entity(class_name=j.class_name, classification=j.classification, identity=j.identity,
                                  level=j.level, opentool=j.opentool, attach=ABattachment(), x=x, y=y)

    def flagToentity(self, reflag: int, id1, id2):
        if current_meta_kg_dict == '教学知识图谱':
            i = relationType_dict['LineType' + str(reflag)]
            return relation(class_name=i.class_name, mask=i.mask, classification=i.classification,
                            head_need=i.head_need,
                            tail_need=i.tail_need, headnodeid=id1, tailnodeid=id2)
        elif current_meta_kg_dict == '能力知识图谱':
            i = relationType_dict['abLineType' + str(reflag)]
            return relation(class_name=i.class_name, mask=i.mask, classification=i.classification,
                            head_need=i.head_need,
                            tail_need=i.tail_need, headnodeid=id1, tailnodeid=id2)

    def charge_child(self, item):
        if isinstance(item, myGraphicItem) or isinstance(item, QGraphicsTextItem) or \
                isinstance(item, ABmyGraphicItem) or isinstance(item, QGraphicsSimpleTextItem) or \
                isinstance(item, GraphicItemGroup) or isinstance(item, ABGraphicItemGroup) or \
                isinstance(item, myGraphicItemGroup_2):
            return True
        return False

    def charge_group(self, item):
        if isinstance(item, GraphicItemGroup) or isinstance(item, ABGraphicItemGroup):
            return True
        return False

    def dropEvent(self, event):
        if current_kg_name not in knowledge_graphs_class.keys():
            return
        print(event.type())
        event.acceptProposedAction()
        treeView = event.source()
        if treeView is None:
            return
        index = treeView.currentIndex()
        text = treeView.model().data(index)
        item_pos = self.mapToScene(event.pos())
        # 将QPointF的坐标转换为整数
        intX = int(item_pos.x())
        intY = int(item_pos.y())
        # 使用转换后的整数坐标调用itemAt
        item = self.scene().itemAt(item_pos, QTransform())
        # 04/28 方法新节点拖拽事件
        if self.charge_child(item):
            # 确定拖拽的对象是从QTreeView中的哪个条目来的
            while not self.charge_group(item):
                item = item.parentItem()
            self.handleDropOnEntity(item, text)
            item.re_init(item.entity)
        else:
            event.acceptProposedAction()
            entity = self.nameToentity(name=text, x=item_pos.x(), y=item_pos.y())
            if entity is None:
                return
            if current_meta_kg_dict == '教学知识图谱':
                item = GraphicItemGroup(scene=self.gr_scene, entity=entity, x=item_pos.x(), y=item_pos.y())
            elif current_meta_kg_dict == '能力知识图谱':
                item = ABGraphicItemGroup(scene=self.gr_scene, entity=entity, x=item_pos.x(), y=item_pos.y())
            isexist(name='.produrce')
            save_kg(current_kg_name, knowledge_graphs_class[current_kg_name],
                    dir='./.produrce')
            self.gr_scene.add_node(item)

            entity_name = text  # 假定拖拽的文本是实体名称
            self.entityDropped.emit(entity_name)

    def handleDropOnEntity(self, item, text):
        self.is_kg_changed = True
        # 根据text确定需要更新的属性
        if current_meta_kg_dict == '教学知识图谱':
            if '知识 K' in text:
                item.entity.attach.K = not item.entity.attach.K
                self.updateRequest.emit()
            elif '思维 T' in text:
                item.entity.attach.T = not item.entity.attach.T
                self.updateRequest.emit()
            elif '示例 E' in text:
                item.entity.attach.E = not item.entity.attach.E
                self.updateRequest.emit()
            elif '问题 Q' in text:
                item.entity.attach.Q = not item.entity.attach.Q
                self.updateRequest.emit()
            elif '练习 P' in text:
                item.entity.attach.P = not item.entity.attach.P
                self.updateRequest.emit()
            elif '思政 Z' in text:
                item.entity.attach.Z = not item.entity.attach.Z
                self.updateRequest.emit()
        if current_meta_kg_dict == '能力知识图谱':

            def getintext(text, name):
                for i in name:
                    if i in text:
                        return True, i
                return False, None

            name1 = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9']
            name2 = ['Pj', 'Tk']
            if item.entity.class_name == '能力点':
                f, t = getintext(text, name1)
                if f:
                    f2 = item.entity.attach.getbool(text=text)
                    if f2:
                        item.entity.attach.allfalse()
                    else:
                        item.entity.attach.allfalse()
                        item.entity.attach.textto(text=text, f=True)
                    self.updateRequest.emit()
            if item.entity.class_name == '学生任务':
                f, t = getintext(text, name2)
                if f:
                    f2 = item.entity.attach.getbool(text=text)
                    if f2:
                        item.entity.attach.allfalse()
                    else:
                        item.entity.attach.allfalse()
                        item.entity.attach.textto(text=text, f=True)
                    self.updateRequest.emit()

    def wash_item(self, list):
        list2 = []
        list3 = []
        for i in list:
            if isinstance(i, GraphicItemGroup) or isinstance(i, ABGraphicItemGroup):
                list2.append(i)
            if isinstance(i, GraphicEdge):
                list3.append(i)
        return list2, list3

    def copy(self, list1):
        new_node = []
        new_relation = []
        list2, list3 = self.wash_item(list1)
        dict = {}
        for i in list2:
            new = i.copy_itself()
            new_node.append(new)
            dict[i] = new
        for i in list3:
            if i.edge.start_item not in list2 or i.edge.end_item not in list2:
                continue
            itemrelation = Link(scene=self.gr_scene, start_item=dict[i.edge.start_item], end_item=dict[i.edge.end_item],
                                flag=i.edge.flag)
            new_relation.append(itemrelation)
        return new_node, new_relation

    def copy_2(self, list1, list2):
        new_node = []
        new_relation = []
        dict = {}
        for i in list1:
            new = i.copy_itself()
            new_node.append(new)
            dict[i] = new
        for i in list2:
            if i.start_item not in list1 or i.end_item not in list1:
                continue
            itemrelation = Link(scene=self.gr_scene, start_item=dict[i.start_item], end_item=dict[i.end_item],
                                flag=i.flag)
            new_relation.append(itemrelation)
        return new_node, new_relation

    def getparent(self, item):
        if item is None:
            return
        while (1):
            if isinstance(item, GraphicItemGroup) or isinstance(item, GraphicEdge) or isinstance(item,
                                                                                                 ABGraphicItemGroup):
                return item
            item = item.parentItem()

    def create_rightmenu(self, pos):
        print(pos)
        item_list = self.scene().selectedItems()
        print('1111', item_list)
        # item_list.append(self.getparent(self.itemAt(pos)))
        if len(item_list) < 1 and isinstance(self.itemAt(pos), GraphicEdge):
            i = self.itemAt(pos)
            if self.draw_link_flag != 0 and self.drag_link is not None:
                self.drag_link.remove()
                self.drag_link = None
            isexist(name='.produrce')
            save_kg(current_kg_name, knowledge_graphs_class[current_kg_name],
                    dir='./.produrce')
            self.gr_scene.remove_link(i)
            self.relationRemove.emit(i.edge.head_entity, i.edge.tail_entity)
            return
        self.groupBox_menu = QMenu(self)

        self.actionA = QAction(u'复制', self)  # 创建菜单选项对象
        self.actionA.setShortcut('Ctrl+C')  # 设置动作A的快捷键
        self.groupBox_menu.addAction(self.actionA)  # 把动作A选项对象添加到菜单self.groupBox_menu上

        self.actionB = QAction(u'删除节点', self)
        self.groupBox_menu.addAction(self.actionB)

        self.actionC = QAction(u'粘贴', self)  # 创建菜单选项对象
        self.actionC.setShortcut('Ctrl+v')  # 设置动作A的快捷键
        self.groupBox_menu.addAction(self.actionC)

        self.actionD = QAction(u'水平对齐', self)
        self.groupBox_menu.addAction(self.actionD)

        self.actionE = QAction(u'水平均布', self)
        self.groupBox_menu.addAction(self.actionE)

        self.actionF = QAction(u'垂直对齐', self)
        self.groupBox_menu.addAction(self.actionF)

        self.actionG = QAction(u'垂直均布', self)
        self.groupBox_menu.addAction(self.actionG)

        # self.actionA.triggered.connect(self.button)  # 将动作A触发时连接到槽函数 button
        self.actionB.triggered.connect(lambda: self.button_2(item_list))
        self.actionA.triggered.connect(lambda: self.button_1(item_list, pos))
        self.actionC.triggered.connect(lambda: self.button_3(pos))
        self.actionD.triggered.connect(lambda: self.button_4(item_list))
        self.actionE.triggered.connect(lambda: self.button_5(item_list))
        self.actionF.triggered.connect(lambda: self.button_6(item_list))
        self.actionG.triggered.connect(lambda: self.button_7(item_list))

        self.groupBox_menu.popup(QCursor.pos())  # 声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以

    def sortentity(self, list, s: str):
        b = []
        for i in list:
            if isinstance(i, GraphicItemGroup) or isinstance(i, ABGraphicItemGroup):
                a = []
                a.append(i)
                a.append(i.pos().x())
                a.append(i.pos().y())
                b.append(a)
        if s == 'x':
            return sorted(b, key=(lambda b: b[1]))
        if s == 'y':
            return sorted(b, key=(lambda b: b[2]))

    def button_7(self, list):
        ent, rela = self.wash_item(list)
        if len(ent) <= 1:
            return
        ent = self.sortentity(ent, 'y')
        min = ent[0][2]
        max = ent[len(ent) - 1][2]
        avg = (max - min) / (len(ent) - 1)
        num = 0
        for i in ent:
            i[0].setcentpos(x=i[0].pos().x(), y=min + avg * num)
            num = num + 1
            i[0].update()
        self.gr_scene.update_links()
        self.move.emit(True)

    def button_6(self, list):
        ent, rela = self.wash_item(list)
        if len(ent) <= 1:
            return
        min = ent[0].pos().x()
        for i in ent:
            if min > i.pos().x():
                min = i.pos().x()
        for i in ent:
            i.setcentpos(x=min, y=i.pos().y())
            i.update()
        self.gr_scene.update_links()
        self.move.emit(True)

    def button_5(self, list):
        ent, rela = self.wash_item(list)
        if len(ent) <= 1:
            return
        ent = self.sortentity(ent, 'x')
        min = ent[0][1]
        max = ent[len(ent) - 1][1]
        avg = (max - min) / (len(ent) - 1)
        num = 0
        for i in ent:
            i[0].setcentpos(x=min + avg * num, y=i[0].pos().y())
            num = num + 1
            i[0].update()
        self.gr_scene.update_links()
        self.move.emit(True)

    def button_4(self, list):
        ent, rela = self.wash_item(list)
        if len(ent) <= 1:
            return
        min = ent[0].pos().y()
        for i in ent:
            if min > i.pos().y():
                min = i.pos().y()
        for i in ent:
            i.setcentpos(x=i.pos().x(), y=min)
            i.update()
        self.gr_scene.update_links()
        self.move.emit(True)

    def button_3(self, pos):
        isexist(name='.produrce')
        save_kg(current_kg_name, knowledge_graphs_class[current_kg_name],
                dir='./.produrce')
        x = self.mapToScene(pos).x() - self.list_of_copy[0].x()
        y = self.mapToScene(pos).y() - self.list_of_copy[0].y()
        ent, rela = self.copy_2(self.list_of_copy[1], self.list_of_copy[2])
        for i in ent:
            if isinstance(i, GraphicItemGroup) or isinstance(i, ABGraphicItemGroup):
                i.setcentpos(i.pos().x() + x, i.pos().y() + y)
                self.gr_scene.add_node(i)
                i.setSelected(True)
        for i in rela:
            if isinstance(i, Link):
                i.scene.add_link(i.gr_edge)
                i.store(self.flagToentity(reflag=i.flag, id1=i.start_item.entity.id,
                                          id2=i.end_item.entity.id))  # 保存最终产生的连接线
                i.update_positions()
        save_kg(name=current_kg_name, kg=knowledge_graphs_class[current_kg_name],
                dir='./temp')
        self.gr_scene.update_kg()

    def button_1(self, select_item_list, pos):
        self.list_of_copy.clear()
        list1, list2 = self.copy(select_item_list)
        self.list_of_copy.append(copy.deepcopy(self.mapToScene(pos)))
        self.list_of_copy.append(list1)
        self.list_of_copy.append(list2)
        pass

    def button_2(self, item_list):
        isexist(name='.produrce')
        save_kg(current_kg_name, knowledge_graphs_class[current_kg_name],
                dir='./.produrce')
        for i in item_list:
            if isinstance(i, GraphicEdge):
                continue
            if isinstance(i, GraphicItemGroup) or isinstance(i, ABGraphicItemGroup):
                self.gr_scene.remove_node(i)
        self.move.emit(True)

    def mousePressEvent(self, event: QtGui.QMouseEvent):

        item = self.get_item_at_click(event)
        print(item)
        # elif self.draw_link_flag != 0:
        #     if isinstance(item, myGraphicItem):
        #         if self.drag_link is None:
        #             self.edge_drag_start(item.Group)
        #         else:
        #             self.edge_drag_end(item.Group)
        #     if isinstance(item, GraphicItemGroup):
        #         if self.drag_link is None:
        #             self.edge_drag_start(item)
        #         else:
        #             self.edge_drag_end(item)
        # else:
        #     super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            if self.draw_link_flag != 0:
                if isinstance(item, myGraphicItem) or isinstance(item, QGraphicsTextItem) or isinstance(item,
                                                                                                        ABmyGraphicItem):
                    if self.drag_link is None:
                        self.edge_drag_start(item.group())
                    else:
                        self.edge_drag_end(item.group())
                elif isinstance(item, GraphicItemGroup) or isinstance(item, ABGraphicItemGroup):
                    if self.drag_link is None:
                        self.edge_drag_start(item)
                    else:
                        self.edge_drag_end(item)
                event.accept()  # 确保事件不会继续传播
            elif item is not None:
                super().mousePressEvent(event)
            elif item is None:
                if self.drag_flag == 0:
                    super().mousePressEvent(event)
                    event.accept()
                elif self.drag_flag == 1:
                    # 如果没有点击图形项，则启动拖拽视图操作
                    self.dragging = True
                    self.lastMousePosition = event.pos()
                    self.setCursor(Qt.ClosedHandCursor)  # 修改鼠标图标为闭合手形
                    super().mousePressEvent(event)
                    event.accept()  # 确保事件不会继续传播
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        pos = event.pos()
        if self.draw_link_flag != 0 and self.drag_link is not None:
            sc_pos = self.mapToScene(pos)
            self.drag_link.gr_edge.set_dst(sc_pos.x(), sc_pos.y())
            self.drag_link.gr_edge.update()
        elif self.dragging:
            # 计算鼠标移动的偏移量
            delta = event.pos() - self.lastMousePosition
            self.lastMousePosition = event.pos()

            # 使用scroll方法来移动视图
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.dragging:
                self.dragging = False
                self.setCursor(Qt.ArrowCursor)  # 鼠标释放后恢复默认图标
        super().mouseReleaseEvent(event)

    def get_item_at_click(self, event):
        """ 获取点击位置的图元，无则返回None. """
        pos = event.pos()
        item = self.itemAt(pos)
        return item

    def edge_drag_start(self, item):
        self.drag_start_item = item  # 拖拽开始时的图元，此属性可以不在__init__中声明
        self.drag_link = Link(self.gr_scene, self.drag_start_item, None,
                              flag=self.draw_link_flag)  # 开始拖拽线条，注意到拖拽终点为None
        self.drag_link.scene.add_link(self.drag_link.gr_edge)

    def LinkisRight(self, h_item, t_item, flag):
        if current_meta_kg_dict == '教学知识图谱':
            i = relationType_dict['LineType' + str(flag)]
            if h_item.entity.id == t_item.entity.id:
                return False
            if h_item.entity.classification != i.head_need or t_item.entity.classification != i.tail_need:
                return False
            return True
        elif current_meta_kg_dict == '能力知识图谱':
            return True

    def edge_drag_end(self, item):
        print("进行关系保存")
        if not self.LinkisRight(self.drag_start_item, item, self.draw_link_flag):
            print('线型错误')
            return
        new_edge = Link(self.gr_scene, self.drag_start_item, item, flag=self.draw_link_flag)  # 拖拽结束
        self.drag_link.remove()  # 删除拖拽时画的线
        self.drag_link = None
        # new_edge.store()  # 保存最终产生的连接线
        isexist(name='.produrce')
        save_kg(current_kg_name, knowledge_graphs_class[current_kg_name],
                dir='./.produrce')
        new_edge.scene.add_link(new_edge.gr_edge)
        new_edge.store(self.flagToentity(reflag=new_edge.flag, id1=new_edge.start_item.entity.id,
                                         id2=new_edge.end_item.entity.id))  # 保存最终产生的连接线
        save_kg(name=current_kg_name, kg=knowledge_graphs_class[current_kg_name],
                dir='./temp')
        print('关系保存结束')
        self.relationAdded.emit(new_edge.head_entity, new_edge.tail_entity)


class GraphicItemGroup(QGraphicsItemGroup):
    def __init__(self, scene: GraphicScene, x, y, entity: entity, parent=None):
        super(GraphicItemGroup, self).__init__(parent)
        self.scene = scene
        self.classtype = 1
        self.name = entity.class_name
        self.entity = entity
        self.attach = entity.attach
        self.class_ = 'KA'
        self.attachment = []
        self.font_text2 = QFont("Arial", 18, QFont.Bold)
        # font.setFamily("SimHei")
        self.start_heightth = 18
        self.bais = 2
        self.start_width = 12
        self.font_text2.setBold(True)
        self.get_class(entity.class_name)
        if self.classtype == 1:
            self.GraphicItem1 = myGraphicItem(scene=scene, group=self, type='type1')

            self.GraphicText2 = QGraphicsSimpleTextItem(self.class_)  # 标记
            self.GraphicText2.setBrush(QColor(189, 53, 61))
            self.GraphicText2.setFont(self.font_text2)
            self.GraphicText2.setPos(self.start_width, self.start_heightth)
            font_text1 = QFont("微软雅黑", 12, QFont.Bold)

            self.GraphicText1 = QGraphicsTextItem("请输入内容")  # 文本内容
            self.GraphicText1.setFont(font_text1)
            self.GraphicText1.setTextWidth(
                self.GraphicItem1.boundingRect().width() - self.GraphicText2.boundingRect().width() - self.start_width - self.bais)
            self.GraphicText1.setPos(self.GraphicText2.boundingRect().width() + self.start_width + self.bais,
                                     self.start_heightth)  # 这里再设置位置，就变成了相对group的位置了
            self.GraphicText1.setDefaultTextColor(QColor(0, 0, 0))

            self.GraphicItem1.setZValue(1)
            self.GraphicText1.setZValue(2)
            self.GraphicText2.setZValue(3)
            self.addToGroup(self.GraphicItem1)
            self.addToGroup(self.GraphicText1)
            self.addToGroup(self.GraphicText2)

            self.setFlag(QGraphicsItem.ItemIsSelectable)  # ***设置图元是可以被选择
            self.setFlag(QGraphicsItem.ItemIsMovable)  # ***设置图元是可以被移动
            self.re_init(entity)
            self.setPos(x - self.boundingRect().width() * 0.5, y - self.boundingRect().height() * 0.5)
        else:

            self.item_2 = myGraphicItemGroup_2(text=self.class_, group=self)
            self.item_2.setZValue(1)
            self.addToGroup(self.item_2)
            self.setPos(x - self.boundingRect().width() * 0.5, y - self.boundingRect().height() * 0.5)
            self.setFlag(QGraphicsItem.ItemIsSelectable)  # ***设置图元是可以被选择
            self.setFlag(QGraphicsItem.ItemIsMovable)  # ***设置图元是可以被移动

    def repaint(self) -> None:
        self.update()

    # def boundingRect(self):
    #     return self.GraphicItem1.boundingRect()

    def setPos(self, *__args):
        super().setPos(*__args)
        self.entity.x = self.pos().x()
        self.entity.y = self.pos().y()

    def setcentpos(self, x, y):
        self.setPos(x - self.boundingRect().width() * 0.5, y - self.boundingRect().height() * 0.5)

    def pos(self):
        pos = super().pos()
        pos.setX(pos.x() + self.boundingRect().width() * 0.5)
        pos.setY(pos.y() + self.boundingRect().height() * 0.5)
        return pos

    def get_class(self, name):
        dict1 = {}
        dict1['知识领域'] = 'KA'
        dict1['知识单元'] = 'KU'
        dict1['知识点'] = 'KP'
        dict1['关键知识细节'] = 'KD'
        if name in dict1.keys():
            self.class_ = dict1[name]
            self.classtype = 1
        else:
            if name == '视频':
                self.class_ = 'V'
                pass
            if name == '测试题':
                self.class_ = 'TS'
                pass
            if name == '文档':
                self.class_ = 'TX'
                pass
            self.classtype = 2

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isSelected():
            for gr_edge in self.scene.links:
                if gr_edge is not None:
                    gr_edge.edge.update_positions()
        self.entity.x = self.pos().x()
        self.entity.y = self.pos().y()
        self.scene.scenechanged.emit(True)

    def clearlist(self):
        for i in self.attachment:
            self.removeFromGroup(i)
            self.scene.removeItem(i)
        self.attachment.clear()

    def reinitattach(self):
        num = 0
        heoght = self.start_heightth + self.GraphicText2.boundingRect().height()
        for i in self.attach.restrlist2():
            if i[0]:
                atta = myGraphicItemGroup_2(text=i[1], group=self)
                atta.setZValue(2)
                self.attachment.append(atta)
                self.addToGroup(atta)
                atta.setPos(5 + num * (atta.r + 0), heoght)
            num = num + 1
            if num == 2:
                num = 0
                heoght = heoght + 26

    def copy_itself(self):
        return GraphicItemGroup(scene=self.scene, x=self.pos().x(), y=self.pos().y(), entity=self.entity.copy_itself())

    def re_init(self, entity: entity):
        pos = self.pos()
        print(entity)
        print(self.entity)
        self.clearlist()
        self.entity.class_name = entity.class_name
        self.entity.content = entity.content
        self.entity.attach = entity.attach
        self.name = entity.class_name
        self.GraphicText1.setPlainText(entity.content)
        self.attach = entity.attach
        self.reinitattach()

        self.get_class(self.entity.class_name)
        if self.GraphicText1.boundingRect().height() + self.start_heightth > self.GraphicItem1.boundingRect().height():
            self.GraphicItem1.prepareGeometryChange()
            self.GraphicItem1.length = self.GraphicText1.boundingRect().height() + self.start_heightth
            self.removeFromGroup(self.GraphicItem1)
            self.addToGroup(self.GraphicItem1)
        if self.GraphicText1.boundingRect().height() + self.start_heightth < self.GraphicItem1.boundingRect().height():
            if self.GraphicText1.boundingRect().height() + self.start_heightth < 200 * 0.62:
                self.GraphicItem1.prepareGeometryChange()
                self.GraphicItem1.length = 200 * 0.62
                self.removeFromGroup(self.GraphicItem1)
                self.addToGroup(self.GraphicItem1)
            else:
                self.GraphicItem1.prepareGeometryChange()
                self.GraphicItem1.length = self.GraphicText1.boundingRect().height() + self.start_heightth
                self.removeFromGroup(self.GraphicItem1)
                self.addToGroup(self.GraphicItem1)
        self.repaint()
        self.GraphicItem1.update()
        self.GraphicText2.setText(self.class_)
        self.setcentpos(pos.x(), pos.y())

        self.scene.scenechanged.emit(True)
        self.update()
        self.scene.update()

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent'):
        self.window = my_Ui_Dialog(linetext=self.name, content=self.GraphicText1.toPlainText(), attach=self.attach,
                                   id=self.entity.id, class_type=self.classtype)

        self.window.my_sign1.connect(self.re_init)
        if self.classtype == 2:
            self.window.setfEnable(False)
        self.window.exec()


class myGraphicItem(QGraphicsItem):
    def __init__(self, scene: GraphicScene, group: GraphicItemGroup, text='', type='type1',
                 parent=None):
        super(myGraphicItem, self).__init__(parent)
        self.Group = group
        self.scene = scene
        self.paintwidth = 3
        # self.line_distance = 30
        self.width = 200
        self.length = 200 * 0.62
        self.type = type

    def boundingRect(self):
        penWidth = self.paintwidth
        # self.prepareGeometryChange()#不能在里面加会死循环
        return QRectF(0 - penWidth / 2, 0 - penWidth / 2, penWidth + self.width, penWidth + self.length)

    def paint1(self, painter, Q=QColor(255, 255, 255)):
        painter.setBrush(Q)
        painter.setPen(QPen(QColor(54, 131, 248), self.paintwidth))
        painter.drawRoundedRect(0, 0, self.width, self.length, 30, 30, Qt.AbsoluteSize)  # z坐标位置 长 宽
        # painter.drawLine(0, self.line_distance, self.width, self.line_distance)

    def paint2(self, painter):
        painter.setBrush(QColor(128, 128, 128))
        painter.setPen(QPen(QColor(0, 139, 139), self.paintwidth))
        painter.drawRoundedRect(0, 0, self.width, self.length, 30, 30, Qt.RelativeSize)  # z坐标位置 长 宽
        painter.setPen(QPen(QColor(255, 204, 0), Qt.SolidLine))
        painter.drawLine(0, 20, self.width, 20)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...):
        Q = QColor(255, 255, 255)
        if self.Group.class_ == 'KA':
            Q = QColor(255, 105, 97)
        if self.Group.class_ == 'KU':
            Q = QColor(176, 217, 128)
        if self.Group.class_ == 'KP':
            Q = QColor(189, 181, 225)
        if self.Group.class_ == 'KD':
            Q = QColor(182, 215, 232)
        if self.type == 'type1':
            self.paint1(painter, Q=Q)
        elif self.type == 'type2':
            self.paint2(painter)

    def pos(self):
        return self.Group.pos()


class myGraphicItemGroup_2(QGraphicsItemGroup):
    def __init__(self, group, text='',
                 parent=None):
        super(myGraphicItemGroup_2, self).__init__(parent)
        self.group = group
        self.r = 22
        self.repaint(True, text=text)

    def repaint(self, flag: bool, text=''):
        if flag:
            self.item = QGraphicsEllipseItem(0, 0, self.r, self.r)
            self.item.setBrush(QColor(255, 192, 122))
            self.item.setPen(QColor(180, 199, 231))
            font = QFont()
            font.setFamily("微软雅黑")
            font.setBold(True)
            font.setPointSizeF(10)
            self.GraphicText = QGraphicsSimpleTextItem(text)
            self.GraphicText.setBrush(QColor(192, 0, 0))
            self.GraphicText.setFont(font)
            self.GraphicText.setPos(0.5 * self.r - 0.5 * self.GraphicText.boundingRect().width(),
                                    0.5 * self.r - 0.5 * self.GraphicText.boundingRect().height())
            self.addToGroup(self.item)
            self.addToGroup(self.GraphicText)
            self.setPos(self.group.pos())


class GraphicItem(QGraphicsPixmapItem):
    def __init__(self, scene: GraphicScene, group: GraphicItemGroup, parent=None):
        super().__init__(parent)
        self.Group = group
        self.scene = scene
        self.setpicture()
        self.setFlag(QGraphicsItem.ItemIsSelectable)  # ***设置图元是可以被选择
        self.setFlag(QGraphicsItem.ItemIsMovable)  # ***设置图元是可以被移动
        scale = 50 / self.pix.height()
        self.setScale(scale)
        self.width = scale * self.pix.width()
        self.height = 50

    def setpicture(self):
        self.pix = QPixmap("picture/加号.png")
        self.setPixmap(self.pix)

    def pos(self):
        return self.Group.pos()

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'):
        pass


class ABGraphicItemGroup(QGraphicsItemGroup):
    def __init__(self, scene: GraphicScene, x, y, entity: entity, parent=None):
        super(ABGraphicItemGroup, self).__init__(parent)
        self.scene = scene
        self.classtype = 1
        self.name = entity.class_name
        self.entity = entity
        self.attach = entity.attach
        self.class_ = 'KA'
        self.attachment = []
        self.font_text2 = QFont("Arial", 18, QFont.Bold)
        # font.setFamily("SimHei")
        self.start_heightth = 18
        self.bais = 2
        self.start_width = 12
        self.font_text2.setBold(True)
        self.get_class(entity.class_name)
        if self.classtype == 1:
            self.GraphicItem1 = ABmyGraphicItem(scene=scene, group=self, type='type1')

            self.GraphicText2 = QGraphicsSimpleTextItem(self.class_)  # 标记
            self.GraphicText2.setBrush(QColor(189, 53, 61))
            self.GraphicText2.setFont(self.font_text2)
            self.GraphicText2.setPos(self.start_width, self.start_heightth)
            font_text1 = QFont("微软雅黑", 12, QFont.Bold)

            self.GraphicText1 = QGraphicsTextItem("请输入内容")  # 文本内容
            self.GraphicText1.setFont(font_text1)
            self.GraphicText1.setTextWidth(
                self.GraphicItem1.boundingRect().width() - self.GraphicText2.boundingRect().width() - self.start_width - self.bais)
            self.GraphicText1.setPos(self.GraphicText2.boundingRect().width() + self.start_width + self.bais,
                                     self.start_heightth)  # 这里再设置位置，就变成了相对group的位置了
            self.GraphicText1.setDefaultTextColor(QColor(0, 0, 0))

            self.GraphicItem1.setZValue(1)
            self.GraphicText1.setZValue(2)
            self.GraphicText2.setZValue(3)
            self.addToGroup(self.GraphicItem1)
            self.addToGroup(self.GraphicText1)
            self.addToGroup(self.GraphicText2)

            self.setFlag(QGraphicsItem.ItemIsSelectable)  # ***设置图元是可以被选择
            self.setFlag(QGraphicsItem.ItemIsMovable)  # ***设置图元是可以被移动
            self.re_init(entity)
            self.setPos(x - self.boundingRect().width() * 0.5, y - self.boundingRect().height() * 0.5)
        else:

            self.item_2 = myGraphicItemGroup_2(text=self.class_, group=self)
            self.item_2.setZValue(1)
            self.addToGroup(self.item_2)
            self.setPos(x - self.boundingRect().width() * 0.5, y - self.boundingRect().height() * 0.5)
            self.setFlag(QGraphicsItem.ItemIsSelectable)  # ***设置图元是可以被选择
            self.setFlag(QGraphicsItem.ItemIsMovable)  # ***设置图元是可以被移动

    def repaint(self) -> None:
        self.update()

    # def boundingRect(self):
    #     return self.GraphicItem1.boundingRect()

    def setPos(self, *__args):
        super().setPos(*__args)
        self.entity.x = self.pos().x()
        self.entity.y = self.pos().y()

    def setcentpos(self, x, y):
        self.setPos(x - self.boundingRect().width() * 0.5, y - self.boundingRect().height() * 0.5)

    def pos(self):
        pos = super().pos()
        pos.setX(pos.x() + self.boundingRect().width() * 0.5)
        pos.setY(pos.y() + self.boundingRect().height() * 0.5)
        return pos

    def get_class(self, name):
        dict1 = {}
        dict1['能力领域'] = 'CA'
        dict1['能力单元'] = 'CU'
        dict1['能力点'] = 'CP'
        dict1['学生任务'] = 'SJ'
        dict1['知识点'] = 'KP'
        if name in dict1.keys():
            self.class_ = dict1[name]
            self.classtype = 1
        else:
            if name == '视频':
                self.class_ = 'V'
                pass
            if name == '测试题':
                self.class_ = 'TS'
                pass
            if name == '文档':
                self.class_ = 'TX'
                pass
            self.classtype = 2

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isSelected():
            for gr_edge in self.scene.links:
                if gr_edge is not None:
                    gr_edge.edge.update_positions()
        self.entity.x = self.pos().x()
        self.entity.y = self.pos().y()
        self.scene.scenechanged.emit(True)

    def clearlist(self):
        for i in self.attachment:
            self.removeFromGroup(i)
            self.scene.removeItem(i)
        self.attachment.clear()

    def reinitattach(self):
        num = 0
        heoght = self.start_heightth + self.GraphicText2.boundingRect().height()
        for i in self.attach.restrlist2():
            if i[0]:
                atta = myGraphicItemGroup_2(text=i[1], group=self)
                atta.setZValue(2)
                self.attachment.append(atta)
                self.addToGroup(atta)
                atta.setPos(5 + num * (atta.r + 0), heoght)
                num = num + 1
            if num == 3:
                num = 0
                heoght = heoght + 26

    def copy_itself(self):
        return ABGraphicItemGroup(scene=self.scene, x=self.pos().x(), y=self.pos().y(),
                                  entity=self.entity.copy_itself())

    def re_init(self, entity: entity):
        pos = self.pos()
        print(entity)
        print(self.entity)
        self.clearlist()
        self.entity.class_name = entity.class_name
        self.entity.content = entity.content
        self.entity.attach = entity.attach
        self.name = entity.class_name
        self.GraphicText1.setPlainText(entity.content)
        self.attach = entity.attach
        self.reinitattach()

        self.get_class(self.entity.class_name)
        if self.GraphicText1.boundingRect().height() + self.start_heightth > self.GraphicItem1.boundingRect().height():
            self.GraphicItem1.prepareGeometryChange()
            self.GraphicItem1.length = self.GraphicText1.boundingRect().height() + self.start_heightth
            self.removeFromGroup(self.GraphicItem1)
            self.addToGroup(self.GraphicItem1)
        if self.GraphicText1.boundingRect().height() + self.start_heightth < self.GraphicItem1.boundingRect().height():
            if self.GraphicText1.boundingRect().height() + self.start_heightth < 200 * 0.62:
                self.GraphicItem1.prepareGeometryChange()
                self.GraphicItem1.length = 200 * 0.62
                self.removeFromGroup(self.GraphicItem1)
                self.addToGroup(self.GraphicItem1)
            else:
                self.GraphicItem1.prepareGeometryChange()
                self.GraphicItem1.length = self.GraphicText1.boundingRect().height() + self.start_heightth
                self.removeFromGroup(self.GraphicItem1)
                self.addToGroup(self.GraphicItem1)
        self.repaint()
        self.GraphicItem1.update()
        self.GraphicText2.setText(self.class_)
        self.setcentpos(pos.x(), pos.y())

        self.scene.scenechanged.emit(True)
        self.update()
        self.scene.update()

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent'):
        self.window = ABmy_Ui_Dialog(linetext=self.name, content=self.GraphicText1.toPlainText(), attach=self.attach,
                                     id=self.entity.id, class_type=self.classtype)

        self.window.my_sign1.connect(self.re_init)
        if self.classtype == 2:
            self.window.setfEnable(False)
        self.window.exec()


class ABmyGraphicItem(QGraphicsItem):
    def __init__(self, scene: GraphicScene, group: ABGraphicItemGroup, text='', type='type1',
                 parent=None):
        super(ABmyGraphicItem, self).__init__(parent)
        self.Group = group
        self.scene = scene
        self.paintwidth = 3
        # self.line_distance = 30
        self.width = 200
        self.length = 200 * 0.62
        self.type = type

    def boundingRect(self):
        penWidth = self.paintwidth
        return QRectF(0 - penWidth / 2, 0 - penWidth / 2, penWidth + self.width, penWidth + self.length)

    def paint1(self, painter, Q=QColor(255, 255, 255)):
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(QPen(Q, self.paintwidth))
        painter.drawRoundedRect(0, 0, self.width, self.length, 30, 30, Qt.AbsoluteSize)  # z坐标位置 长 宽
        # painter.drawLine(0, self.line_distance, self.width, self.line_distance)

    # def paint2(self, painter):
    #     painter.setBrush(QColor(128, 128, 128))
    #     painter.setPen(QPen(QColor(0, 139, 139), self.paintwidth))
    #     painter.drawRoundedRect(0, 0, self.width, self.length, 30, 30, Qt.RelativeSize)  # z坐标位置 长 宽
    #     painter.setPen(QPen(QColor(255, 204, 0), Qt.SolidLine))
    #     painter.drawLine(0, 20, self.width, 20)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...):
        Q = QColor(255, 255, 255)
        if self.Group.class_ == 'CA':
            Q = QColor(255, 105, 97)
        if self.Group.class_ == 'CU':
            Q = QColor(176, 217, 128)
        if self.Group.class_ == 'CP':
            Q = QColor(189, 181, 225)
        if self.Group.class_ == 'SJ':
            Q = QColor(182, 215, 232)
        if self.Group.class_ == 'KP':
            Q = QColor(0, 0, 0)
        # if self.Group.class_ == '任务':
        #     Q = QColor(153, 153, 153)
        # if self.Group.class_ == '知识点':
        #     Q = QColor(0, 0, 0)
        self.paint1(painter, Q=Q)
        # elif self.type == 'type2':
        #     self.paint2(painter)

    def pos(self):
        return self.Group.pos()


class Link:
    def __init__(self, scene: GraphicScene, start_item: typing.Union[GraphicItemGroup, ABGraphicItemGroup],
                 end_item: typing.Union[GraphicItemGroup, ABGraphicItemGroup, None],
                 flag: int):
        # 参数分别为场景、开始图元、结束图元
        super().__init__()
        self.scene = scene
        self.start_item = start_item
        self.end_item = end_item
        self.flag = flag
        # 线条图形在此处创建
        self.gr_edge = GraphicEdge(self)

        self.head_entity = " "
        self.tail_entity = " "
        # 此类一旦被初始化就在添加进scene

        # 开始更新
        if self.start_item is not None:
            self.update_positions()

    # 最终保存进scene
    def store(self, relation: relation):
        self.relation = relation
        self.head_entity = self.start_item.name
        self.tail_entity = self.end_item.name

    def flagToentity(self):
        reflag = self.flag
        id1 = self.start_item.entity.id
        id2 = self.end_item.entity.id
        if current_meta_kg_dict == '教学知识图谱':
            i = relationType_dict['LineType' + str(reflag)]
        if current_meta_kg_dict == '能力知识图谱':
            i = relationType_dict['abLineType' + str(reflag)]
        self.store(
            relation(class_name=i.class_name, mask=i.mask, classification=i.classification, head_need=i.head_need,
                     tail_need=i.tail_need, headnodeid=id1, tailnodeid=id2))

    # 更新位置
    def update_positions(self):
        # src_pos 记录的是开始图元的位置，此位置为图元的左上角
        src_pos = self.start_item.pos()
        # 想让线条从图元的中心位置开始，让他们都加上偏移
        self.gr_edge.set_src(src_pos.x(), src_pos.y())
        # 如果结束位置图元也存在，则做同样操作
        if self.end_item is not None:
            end_pos = self.end_item.pos()
            self.gr_edge.set_dst(end_pos.x(), end_pos.y())
        else:
            self.gr_edge.set_dst(src_pos.x(), src_pos.y())
        self.gr_edge.update()

    def remove_from_current_items(self):
        self.end_item = None
        self.start_item = None

    # 移除线条
    def remove(self):
        self.scene.remove_link(self.gr_edge)
        # self.remove_from_current_items()
        self.gr_edge = None


class GraphicEdge(QGraphicsPathItem):
    def __init__(self, edge_wrap: Link, relation_id=0, parent=None, text=''):
        super().__init__(parent)
        # 这个参数是GraphicEdge的包装类，见下文
        self.edge = edge_wrap
        self.width = 2  # 线条的宽度
        self.pos_src = [0, 0]  # 线条起始位置 x，y坐标
        self.pos_dst = [0, 0]  # 线条结束位置
        self.id = relation_id
        self._mark_pen = QPen(Qt.black)
        self._mark_pen.setWidthF(1.2)
        self._mark_brush = QBrush()
        self._mark_brush.setColor(Qt.black)
        self._mark_brush.setStyle(Qt.SolidPattern)
        self._pen = QPen(QColor("#000"))  # 画线条的
        self._pen.setWidthF(self.width)
        self.text = text
        if self.edge.flag == 1:
            self._pen = QPen(QColor("#000"))  # 画线条的
            self._pen.setWidthF(self.width)
            self._mark_pen = QPen(QColor("#000"))

        if self.edge.flag == 2:
            self._pen = QPen(QColor(0, 0, 196))  # 画线条的
            self._pen.setWidthF(self.width)
            self._mark_pen = QPen(QColor(0, 0, 196))

        if self.edge.flag == 3:
            self._pen = QPen(QColor(0, 196, 0))  # 画线条的
            self._pen.setWidthF(self.width)
            self._pen.setStyle(Qt.DashDotLine)
            self._mark_pen = QPen(QColor(0, 196, 0))

        if self.edge.flag == 4:
            self._pen = QPen(QColor(0, 0, 0))  # 画线条的
            self._pen.setWidthF(self.width * 3)
            self._mark_pen = QPen(QColor(0, 0, 0))
            self._mark_pen.setWidthF(3.6)

        if self.edge.flag == 5:
            self._pen = QPen(QColor(139, 0, 0))  # 画线条的
            self._pen.setWidthF(self.width)
            self._pen.setStyle(Qt.DashDotLine)
            self._mark_pen = QPen(QColor(139, 0, 0))

        if self.edge.flag == 6:
            self._pen = QPen(QColor(0, 0, 0))  # 画线条的
            self._pen.setWidthF(self.width)
            self._pen.setStyle(Qt.DashDotLine)
            self._mark_pen = QPen(QColor(0, 0, 0))

        self._pen_dragging = QPen(QColor("#000"))  # 画拖拽线条时线条的
        self._pen_dragging.setStyle(Qt.DashDotLine)
        self._pen_dragging.setWidthF(self.width)

        self.setFlag(QGraphicsItem.ItemIsSelectable)  # 线条可选
        self.setZValue(-1)  # 让线条出现在所有图元的最下层

    def set_src(self, x, y):
        self.pos_src = [x, y]

    def set_dst(self, x, y):
        self.pos_dst = [x, y]

    # 计算线条的路径
    def calc_path(self):
        path = QPainterPath(QPointF(self.pos_src[0], self.pos_src[1]))  # 起点
        path.lineTo(self.pos_dst[0], self.pos_dst[1])  # 终点
        return path

    # override
    def boundingRect(self):
        self.shape().boundingRect()
        return self.shape().boundingRect()

    # override
    def shape(self):
        stker = QPainterPathStroker()
        stker.setWidth(7)
        stker.createStroke(self.calc_path())
        return stker.createStroke(self.calc_path())

    def get_distance(self, x, y, k):
        if math.sin(k) == 0:
            return x * 0.5
        if math.cos(k) == 0:
            return y * 0.5
        a1 = math.fabs(y / (math.sin(k) * 2))
        a2 = math.fabs(x / (math.cos(k) * 2))
        if a2 > a1:
            return a1
        else:
            return a2

    def draw_arrow(self, length, point, painter, k):
        point1 = point
        new_x = point1.x()
        new_y = point1.y()
        length_arrow = length
        new_x1 = new_x - length_arrow * math.cos(k - np.pi / 8)
        new_y1 = new_y - length_arrow * math.sin(k - np.pi / 8)
        new_x2 = new_x - length_arrow * math.cos(k + np.pi / 8)
        new_y2 = new_y - length_arrow * math.sin(k + np.pi / 8)
        painter.setPen(self._mark_pen)
        painter.setBrush(self._mark_brush)
        point2 = QPoint((new_x1), (new_y1))
        point3 = QPoint((new_x2), (new_y2))
        points = []
        points.append(point2)
        points.append(point1)
        points.append(point3)
        painter.drawPolyline(point2, point1, point3)

    def degreeToDegree(self, k):
        if k < 0:
            return 360 + k
        return k

    def draw_arc(self, point: QPointF, painter, k):
        point1 = point
        h = 8
        w = 8
        k1 = -math.degrees(k) - 45
        painter.drawArc(point1.x() - w, point1.y() - h, 2 * w, 2 * h, k1 * 16, 90 * 16)

    def paint_angle(self, painter):
        x1, y1 = self.pos_src
        x2, y2 = self.pos_dst
        a = x2 - x1
        b = y2 - y1
        k = math.atan2(y2 - y1, x2 - x1)  # theta
        length = self.get_distance(self.edge.end_item.boundingRect().width(),
                                   self.edge.end_item.boundingRect().height(), k)  # 圆点距离终点图元的距离
        point1 = self.path().pointAtPercent(self.path().percentAtLength(math.sqrt(a * a + b * b) - length))
        if self.edge.flag == 1:
            point2 = self.path().pointAtPercent(0.5)
            # self.draw_arrow(length=10, point=point2, painter=painter, k=k)
            # point3 = self.path().pointAtPercent(self.path().percentAtLength(0.5 * math.sqrt(a * a + b * b) + 10))
            # self.draw_arrow(length=10, point=point3, painter=painter, k=k)
            self.draw_arc(point=point2, painter=painter, k=k)
        elif self.edge.flag == 4:
            self.draw_arrow(length=30, point=point1, painter=painter, k=k)
        else:
            self.draw_arrow(length=10, point=point1, painter=painter, k=k)

    # override
    def paint(self, painter, graphics_item, widget=None):
        self.setPath(self.calc_path())  # 设置路径
        path = self.path()
        if self.edge.end_item is None:
            # 包装类中存储了线条开始和结束位置的图元
            # 刚开始拖拽线条时，并没有结束位置的图元，所以是None
            # 这个线条画的是拖拽路径，点线
            painter.setPen(self._pen_dragging)
            painter.drawPath(path)
        else:
            # 这画的才是连接后的线
            painter.setPen(self._pen)
            painter.drawPath(path)
            painter.drawText(self.path().pointAtPercent(0.5), '')
            self.paint_angle(painter)
