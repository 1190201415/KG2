# -*-coding = utf-8 -*-
# @Time : 2024/2/19 17:42
# @Author :skq
# @File : Myclass.py
# @Software: PyCharm
import math
import os
import typing
from pathlib import Path

import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsEllipseItem, \
    QGraphicsItem, QTreeView, QGraphicsPathItem, QGraphicsItemGroup, QGraphicsSimpleTextItem, QWidget, \
    QGraphicsTextItem, \
    QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent, QDialog
from PyQt5.QtCore import Qt, QLine, QPointF, QPoint, pyqtSignal, QRectF
from PyQt5.QtGui import QColor, QPen, QPainter, QPixmap, QPainterPath, QBrush, QFont
from entity1 import Ui_Dialog
import xml.etree.ElementTree as ET

entityType_dict = {}
relationType_dict = {}
knowledge_graphs_class = {
    "知识图谱1": {
        "entities": [],
        "relations": []
    },
}
current_kg_name = '知识图谱1'
node_id = 0


class attachment(object):
    def __init__(self, K=False, T=False, Z=False, E=False, Q=False, P=False):
        self.T = T
        self.Z = Z
        self.Q = Q
        self.K = K
        self.E = E
        self.P = P

    def tostring(self):
        str1 = ''
        attri = vars(self)
        for a, v in attri.items():
            if v:
                str1 = str1 + '1'
            else:
                str1 = str1 + '0'
        return str1

    def tobool(self, str):
        if str == '0':
            return False
        if str == '1':
            return True

    def stringTo(self, str):
        attri = vars(self)
        num = 0
        for a, v in attri.items():
            setattr(self, a, self.tobool(str[num]))
            num = num + 1


class relationType(object):
    def __init__(self, class_name='包含关系', mask='知识连线', classification='包含关系', head_need='内容方法型节点', tail_need='内容方法型节点'):
        self.class_name = class_name
        self.mask = mask
        self.classification = classification
        self.head_need = head_need
        self.tail_need = tail_need


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
    def __init__(self, attach: attachment, x: int, y: int, content='无', class_name='知识单元', classification='内容方法型',
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


class my_treeview(QTreeView):
    my_sign_kg = pyqtSignal()

    def __init__(self, scence, parent=None, ):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.scence = scence

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent):
        if e.mimeData().hasText():
            e.acceptProposedAction()
        else:
            e.ignore()

    def dragMoveEvent(self, event: QtGui.QMouseEvent):
        event.accept()

    def find_item(self, name, id):
        print('z', id)
        entities = knowledge_graphs_class[name]['entities']
        for i in entities:
            if id == i.entity.id:
                print(id, i)
                return i

    def class_nameToflag(self, class_name):
        dict1 = {'包含关系': 1, '次序关系': 2, '连接资源': 3}

        return dict1[class_name]

    def dropEvent(self, e: QtGui.QDropEvent):
        e.acceptProposedAction()
        filePathList = e.mimeData().text()
        filePath = filePathList.split('\n')[0]  # 拖拽多文件只取第一个地址
        filePath = filePath.replace('file:///', '', 1)  # 去除文件地址前缀的特定字符
        tree = ET.parse(filePath)  # 解析movies.xml这个文件
        filePath = Path(filePath)
        root = tree.getroot()  # 得到根元素，Element类
        entities = root.findall('entities')
        relations = root.findall('relations')
        entitys = entities[0].findall('entity')
        now_kg_name = os.path.basename(filePath).split('.')[0]
        if now_kg_name not in knowledge_graphs_class.keys():
            knowledge_graphs_class[now_kg_name] = {"entities": [], "relations": []}
        relations1 = relations[0].findall('relation')
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
            itemgroup = GraphicItemGroup(scene=self.scence, entity=entity1, x=entity1.x, y=entity1.y)
            itemgroup.setPos(entity1.x, entity1.y)
            knowledge_graphs_class[now_kg_name]['entities'].append(itemgroup)
        for i in relations1:
            relation1 = relation()
            for j in i:
                if hasattr(relation1, j.tag):
                    setattr(relation1, j.tag, j.text)
            itemrelation = Link(scene=self.scence, start_item=self.find_item(now_kg_name, int(relation1.headnodeid)),
                                end_item=self.find_item(now_kg_name, int(relation1.tailnodeid)),
                                flag=self.class_nameToflag(relation1.class_name))
            itemrelation.flagToentity()
            knowledge_graphs_class[now_kg_name]['relations'].append(itemrelation)
        self.scence.update_kg()
        self.my_sign_kg.emit()


class my_Ui_Dialog(QDialog, Ui_Dialog):
    my_sign1 = pyqtSignal(entity)

    def __init__(self, parent=None, linetext='', content='', attach=attachment(), id=0):
        super(my_Ui_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.label_4.setText(str(id))
        self.lineEdit.setText(linetext)
        self.textEdit.setText(content)
        self.checkBox.setChecked(attach.K)
        self.checkBox_2.setChecked(attach.T)
        self.checkBox_3.setChecked(attach.Z)
        self.checkBox_4.setChecked(attach.E)
        self.checkBox_5.setChecked(attach.Q)
        self.checkBox_6.setChecked(attach.P)
        self.pushButton.clicked.connect(self.clickpushbutton)
        self.pushButton_2.clicked.connect(self.clickpushbutton_2)

    def clickpushbutton(self):
        name = self.lineEdit.text()
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

    def clickpushbutton_2(self):
        self.close()


class GraphicScene(QGraphicsScene):
    entityRemove = pyqtSignal(str)

    def __init__(self, parent=None, ):
        super().__init__(parent)
        self.nodes = []
        self.links = []
        # 一些关于网格背景的设置
        self.grid_size = 20  # 一块网格的大小 （正方形的）
        self.grid_squares = 5  # 网格中正方形的区域个数

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
        ax = 0
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

    def add_node(self, node):
        if node not in self.nodes:
            # self.mainwindow.entity_dict.a
            self.nodes.append(node)
            self.addItem(node)
            print(node)
            knowledge_graphs_class[current_kg_name]['entities'].append(node)

    def add_link(self, link):
        if link not in self.links:
            print('添加', link)
            self.links.append(link)
            self.addItem(link)
            knowledge_graphs_class[current_kg_name]['relations'].append(link.edge)

    def remove_node(self, node):
        self.nodes.remove(node)
        self.removeItem(node)
        self.entityRemove.emit(node.name)
        knowledge_graphs_class[current_kg_name]['entities'].remove(node)

    def remove_link(self, link):
        print("删除", link)
        if link in self.links:
            self.links.remove(link)
            self.removeItem(link)
            knowledge_graphs_class[current_kg_name]['relations'].remove(link.edge)

    def saveAll_AS_Xml(self):
        for node in self.nodes:
            print(node.name)
        for link in self.links:
            print(link.id)

    def save_nodes(self):
        return

    def save_links(self):
        return

    def get_all_item(self):
        for item in self.nodes:
            print(item.give_pos())

    # override
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # 获取背景矩形的上下左右的长度，分别向上或向下取整数
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        # 从左边和上边开始
        first_left = left - (left % self.grid_size)  # 减去余数，保证可以被网格大小整除
        first_top = top - (top % self.grid_size)

        # 分别收集明、暗线
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

            # 最后把收集的明、暗线分别画出来
        painter.setPen(self._pen_light)
        if lines_light:
            painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        if lines_dark:
            painter.drawLines(*lines_dark)


class GraphicView(QGraphicsView):
    entityDropped = pyqtSignal(str)  # 假设信号传递实体名称和坐标
    relationAdded = pyqtSignal(str, str)
    relationRemove = pyqtSignal(str, str)

    def __init__(self, graphic_scene: GraphicScene, parent=None):
        super().__init__(parent)
        self.gr_scene = graphic_scene  # 将scene传入此处托管，方便在view中维护
        self.parent = parent

        # 03/23
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)  # 设置拖拽模式为“手形”
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.drag_link: Link = None  # 记录拖拽时的线
        self.draw_link_flag = 0

        self.init_ui()

        self.startItem = None  # 拖拽开始的项（头结点）
        self.endItem = None  # 拖拽结束的项（尾结点）
        self.currentRelationType = None  # 当前关系类型，需要有途径设置

        # 03/23 用于拖拽的变量
        self.dragging = False
        self.lastMousePosition = None

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
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        # 设置拖拽模式
        self.setDragMode(self.RubberBandDrag)
        self.setAcceptDrops(True)

    # 03/23
    def wheelEvent(self, event):
        zoomInFactor = 1.25  # 定义放大的比例因子
        zoomOutFactor = 1 / zoomInFactor  # 定义缩小的比例因子

        # 设置缩放的中心点为当前鼠标位置
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        # 滚轮向上滚动，放大
        if event.angleDelta().y() > 0:
            self.scale(zoomInFactor, zoomInFactor)
        # 滚轮向下滚动，缩小
        else:
            self.scale(zoomOutFactor, zoomOutFactor)

        event.accept()

    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        # current_item = self.parent.itemAt(pos)  # 获取当前坐标下的item
        # current_index = self.parent.indexFromItem(current_item)  # 获取该item的index
        # print(current_index)

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        event.accept()
        # current_item = self.parent.itemAt(pos)  # 获取当前坐标下的item
        # current_index = self.parent.indexFromItem(current_item)  # 获取该item的index
        # print(current_index)

    def nameToentity(self, name, x, y):
        for i in entityType_dict.keys():
            j = entityType_dict[i]
            if name == j.class_name:
                return entity(class_name=j.class_name, classification=j.classification, identity=j.identity,
                              level=j.level, opentool=j.opentool, attach=attachment(), x=x, y=y)

    def flagToentity(self, reflag: int, id1, id2):
        i = relationType_dict['LineType' + str(reflag)]
        return relation(class_name=i.class_name, mask=i.mask, classification=i.classification, head_need=i.head_need,
                        tail_need=i.tail_need, headnodeid=id1, tailnodeid=id2)

    def dropEvent(self, event):
        event.acceptProposedAction()
        treeView = event.source()
        index = treeView.currentIndex()
        text = treeView.model().data(index)
        item_pos = self.mapToScene(event.pos())
        entity = self.nameToentity(name=text, x=item_pos.x(), y=item_pos.y())
        if entity is None:
            return
        item = GraphicItemGroup(scene=self.gr_scene, entity=entity, x=item_pos.x(), y=item_pos.y())
        print(item)
        self.gr_scene.add_node(item)

        entity_name = text  # 假定拖拽的文本是实体名称
        self.entityDropped.emit(entity_name)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        item = self.get_item_at_click(event)
        if event.button() == Qt.RightButton:
            if isinstance(item, myGraphicItem):
                self.gr_scene.remove_node(item.Group)
            if isinstance(item, GraphicItemGroup):
                self.gr_scene.remove_node(item)
            if isinstance(item, GraphicEdge):
                self.gr_scene.remove_link(item)
                self.relationRemove.emit(item.edge.head_entity, item.edge.tail_entity)

            if self.draw_link_flag != 0 and self.drag_link is not None:
                self.drag_link.remove()
                self.drag_link = None
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
        elif event.button() == Qt.LeftButton:
            if self.draw_link_flag != 0:
                if isinstance(item, myGraphicItem):
                    if self.drag_link is None:
                        self.edge_drag_start(item.Group)
                    else:
                        self.edge_drag_end(item.Group)
                if isinstance(item, GraphicItemGroup):
                    if self.drag_link is None:
                        self.edge_drag_start(item)
                    else:
                        self.edge_drag_end(item)
                event.accept()  # 确保事件不会继续传播
            elif item is not None:
                super().mousePressEvent(event)
                event.accept()
            elif item is None:
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
        i = relationType_dict['LineType' + str(flag)]
        if h_item.entity.classification != i.head_need or t_item.entity.classification != i.tail_need:
            return False
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
        new_edge.scene.add_link(new_edge.gr_edge)
        new_edge.store(self.flagToentity(reflag=new_edge.flag, id1=new_edge.start_item.entity.id,
                                         id2=new_edge.end_item.entity.id))  # 保存最终产生的连接线
        print('关系保存结束')
        # self.relationAdded.emit(new_edge.head_entity, new_edge.tail_entity)


class GraphicItemGroup(QGraphicsItemGroup):
    def __init__(self, scene: GraphicScene, x, y, entity: entity, parent=None):
        super(GraphicItemGroup, self).__init__(parent)
        self.scene = scene
        self.classtype = 1
        self.name = entity.class_name
        self.entity = entity
        self.attach = entity.attach
        self.class_ = 'KA'
        self.get_class(entity.class_name)
        self.attachment = []
        font = QFont()
        font.setFamily("SimHei")
        font.setBold(True)
        if self.classtype == 1:
            self.GraphicItem1 = myGraphicItem(scene=scene, group=self, type='type1')
            self.GraphicText2 = QGraphicsSimpleTextItem(self.class_)
            self.GraphicText2.setBrush(QColor(0, 0, 0))
            self.GraphicText2.setFont(font)
            self.GraphicText2.setPos(10, (
                    self.GraphicItem1.line_distance - self.GraphicText2.boundingRect().height()) * 0.5)
        else:
            self.GraphicItem1 = myGraphicItem(scene=scene, group=self, type='type2')
            self.GraphicText2 = QGraphicsSimpleTextItem(self.class_)
            self.GraphicText2.setBrush(QColor(255, 255, 255))
            self.GraphicText2.setFont(font)
            self.GraphicText2.setPos((self.GraphicItem1.width - self.GraphicText2.boundingRect().width()) * 0.5, (
                    self.GraphicItem1.line_distance - self.GraphicText2.boundingRect().height()) * 0.5)
        self.GraphicText1 = QGraphicsTextItem("请输入内容")
        self.GraphicText1.setTextWidth(150)
        self.width = self.GraphicItem1.boundingRect().width()
        self.height = self.GraphicItem1.boundingRect().height()
        self.textwith = self.GraphicText1.boundingRect().width()
        self.GraphicText1.setPos(5,
                                 self.GraphicItem1.line_distance)  # 这里再设置位置，就变成了相对group的位置了
        self.GraphicText1.setDefaultTextColor(QColor(0, 0, 0))
        self.addToGroup(self.GraphicItem1)
        self.addToGroup(self.GraphicText1)
        self.addToGroup(self.GraphicText2)
        self.setFlag(QGraphicsItem.ItemIsSelectable)  # ***设置图元是可以被选择
        self.setFlag(QGraphicsItem.ItemIsMovable)  # ***设置图元是可以被移动
        self.setPos(x - self.width * 0.5, y - self.height * 0.5)
        self.re_init(entity)

    def boundingRect(self):
        return self.GraphicItem1.boundingRect()

    def pos(self):
        pos = super().pos()
        pos.setX(pos.x()+self.boundingRect().width()*0.5)
        pos.setY(pos.y()+self.boundingRect().height()*0.5)
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
                self.class_ = 'VedioClass'
                pass
            if name == '测试题':
                self.class_ = 'TestClass'
                pass
            if name == '文档':
                self.class_ = 'TextClass'
                pass
            self.classtype = 2

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isSelected():
            for gr_edge in self.scene.links:
                print(gr_edge)
                if gr_edge is not None:
                    gr_edge.edge.update_positions()
        self.entity.x = self.pos().x()
        self.entity.y = self.pos().y()

    def re_init(self, entity: entity):
        self.entity.class_name = entity.class_name
        self.entity.content = entity.content
        self.entity.attach = entity.attach
        self.name = entity.class_name
        self.GraphicText1.setPlainText(entity.content)
        self.attach = entity.attach
        num = -1
        if self.attach.K:
            num = num + 1
        if self.attach.K and 'K' not in self.attachment:
            self.itemk = myGraphicItemGroup_2(text='K', group=self)
            self.attachment.append('K')
            self.addToGroup(self.itemk)
            self.itemk.setPos(140 - num * 20, 5)
        if 'K' in self.attachment and not self.attach.K:
            self.removeFromGroup(self.itemk)
            self.scene.removeItem(self.itemk)
            self.attachment.remove('K')
        if self.attach.T:
            num = num + 1
        if self.attach.T and 'T' not in self.attachment:
            self.itemT = myGraphicItemGroup_2(text='T', group=self)
            self.attachment.append('T')
            self.addToGroup(self.itemT)
            self.itemT.setPos(140 - num * 20, 5)
        if 'T' in self.attachment and not self.attach.T:
            self.removeFromGroup(self.itemT)
            self.scene.removeItem(self.itemT)
            self.attachment.remove('T')
        if self.attach.Z:
            num = num + 1
        if self.attach.Z and 'Z' not in self.attachment:
            self.itemZ = myGraphicItemGroup_2(text='Z', group=self)
            self.attachment.append('Z')
            self.addToGroup(self.itemZ)
            self.itemZ.setPos(140 - num * 20, 5)
        if 'Z' in self.attachment and not self.attach.Z:
            self.removeFromGroup(self.itemZ)
            self.scene.removeItem(self.itemZ)
            self.attachment.remove('Z')
        if self.attach.E:
            num = num + 1
        if self.attach.E and 'E' not in self.attachment:
            self.itemE = myGraphicItemGroup_2(text='E', group=self)
            self.attachment.append('E')
            self.addToGroup(self.itemE)
            self.itemE.setPos(140 - num * 20, 5)
        if 'E' in self.attachment and not self.attach.E:
            self.removeFromGroup(self.itemE)
            self.scene.removeItem(self.itemE)
            self.attachment.remove('E')
        if self.attach.Q:
            num = num + 1
        if self.attach.Q and 'Q' not in self.attachment:
            self.itemQ = myGraphicItemGroup_2(text='Q', group=self)
            self.attachment.append('Q')
            self.addToGroup(self.itemQ)
            self.itemQ.setPos(140 - num * 20, 5)
        if 'Q' in self.attachment and not self.attach.Q:
            self.removeFromGroup(self.itemQ)
            self.scene.removeItem(self.itemQ)
            self.attachment.remove('Q')
        if self.attach.P:
            num = num + 1
        if self.attach.P and 'P' not in self.attachment:
            self.itemP = myGraphicItemGroup_2(text='P', group=self)
            self.attachment.append('P')
            self.addToGroup(self.itemP)
            self.itemP.setPos(140 - num * 20, 5)
        if 'P' in self.attachment and not self.attach.P:
            self.removeFromGroup(self.itemP)
            self.scene.removeItem(self.itemP)
            self.attachment.remove('P')
        if self.GraphicText1.boundingRect().height() > 60:
            self.GraphicItem1.length = self.GraphicText1.boundingRect().height() + 30
            self.GraphicItem1.update()

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent'):
        self.window = my_Ui_Dialog(linetext=self.name, content=self.GraphicText1.toPlainText(), attach=self.attach,
                                   id=self.entity.id)
        self.window.my_sign1.connect(self.re_init)
        self.window.exec()


class myGraphicItem(QGraphicsItem):
    def __init__(self, scene: GraphicScene, group: GraphicItemGroup, text='', type='type1',
                 parent=None):
        super(myGraphicItem, self).__init__(parent)
        self.Group = group
        self.scene = scene
        self.line_distance = 30
        self.width = 160
        self.length = 90
        self.type = type

    def boundingRect(self):
        penWidth = 1
        return QRectF(0 - penWidth / 2, 0 - penWidth / 2, penWidth + self.width, penWidth + self.length)

    def paint1(self, painter):
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(QPen(QColor(0, 139, 139), Qt.SolidLine))
        painter.drawRoundedRect(0, 0, self.width, self.length, 30, 30, Qt.RelativeSize)  # z坐标位置 长 宽
        painter.drawLine(0, self.line_distance, self.width, self.line_distance)

    def paint2(self, painter):
        painter.setBrush(QColor(128, 128, 128))
        painter.setPen(QPen(QColor(0, 139, 139), Qt.SolidLine))
        painter.drawRoundedRect(0, 0, self.width, self.length, 30, 30, Qt.RelativeSize)  # z坐标位置 长 宽
        painter.setPen(QPen(QColor(255, 204, 0), Qt.SolidLine))
        painter.drawLine(0, 30, self.width, 30)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...):
        if self.type == 'type1':
            self.paint1(painter)
        elif self.type == 'type2':
            self.paint2(painter)

    def pos(self):
        return self.Group.pos()


class myGraphicItemGroup_2(QGraphicsItemGroup):
    def __init__(self, group, text='',
                 parent=None):
        super(myGraphicItemGroup_2, self).__init__(parent)
        self.item = QGraphicsEllipseItem(0, 0, 20, 20)
        font = QFont()
        font.setFamily("SimHei")
        font.setBold(True)
        self.GraphicText = QGraphicsSimpleTextItem(text)
        self.GraphicText.setBrush(QColor(0, 0, 0))
        self.GraphicText.setFont(font)
        self.GraphicText.setPos(10 - 0.5 * self.GraphicText.boundingRect().width(),
                                10 - 0.5 * self.GraphicText.boundingRect().height())
        self.addToGroup(self.GraphicText)
        self.addToGroup(self.item)
        self.setPos(group.pos())


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


class Treeview(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)


class Link:
    def __init__(self, scene: GraphicScene, start_item: GraphicItemGroup, end_item: GraphicItemGroup, flag: int):
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
        print('保存relation', self, relation)
        self.relation = relation
        self.head_entity = self.start_item.name
        self.tail_entity = self.end_item.name

    def flagToentity(self):
        reflag = self.flag
        id1 = self.start_item.entity.id
        id2 = self.end_item.entity.id
        i = relationType_dict['LineType' + str(reflag)]
        self.store(
            relation(class_name=i.class_name, mask=i.mask, classification=i.classification, head_need=i.head_need,
                     tail_need=i.tail_need, headnodeid=id1, tailnodeid=id2))

    # 更新位置
    def update_positions(self):
        # src_pos 记录的是开始图元的位置，此位置为图元的左上角
        src_pos = self.start_item.pos()
        # 想让线条从图元的中心位置开始，让他们都加上偏移
        self.gr_edge.set_src(src_pos.x() , src_pos.y() )
        # 如果结束位置图元也存在，则做同样操作
        if self.end_item is not None:
            end_pos = self.end_item.pos()
            self.gr_edge.set_dst(end_pos.x() , end_pos.y() )
        else:
            self.gr_edge.set_dst(src_pos.x(), src_pos.y() )
        self.gr_edge.update()

    def remove_from_current_items(self):
        self.end_item = None
        self.start_item = None

    # 移除线条
    def remove(self):
        self.remove_from_current_items()
        self.scene.remove_link(self.gr_edge)
        self.gr_edge = None


class GraphicEdge(QGraphicsPathItem):
    def __init__(self, edge_wrap: Link, relation_id=0, parent=None):
        super().__init__(parent)
        # 这个参数是GraphicEdge的包装类，见下文
        self.edge = edge_wrap
        self.width = 2.0  # 线条的宽度
        self.pos_src = [0, 0]  # 线条起始位置 x，y坐标
        self.pos_dst = [0, 0]  # 线条结束位置
        self.id = relation_id
        self._mark_pen = QPen(Qt.black)
        self._mark_pen.setWidthF(self.width)
        self._mark_brush = QBrush()
        self._mark_brush.setColor(Qt.black)
        self._mark_brush.setStyle(Qt.SolidPattern)
        self._pen = QPen(QColor("#000"))  # 画线条的
        self._pen.setWidthF(self.width)
        if self.edge.flag == 1:
            self._pen = QPen(QColor("#000"))  # 画线条的
            self._pen.setWidthF(self.width)

        if self.edge.flag == 2:
            self._pen = QPen(QColor(0, 0, 196))  # 画线条的
            self._pen.setWidthF(self.width)

        if self.edge.flag == 3:
            self._pen = QPen(QColor(0, 196, 0))  # 画线条的
            self._pen.setWidthF(self.width)

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
        return self.shape().boundingRect()

    # override
    def shape(self):
        return self.calc_path()

    def get_distance(self, x, y):
        return 0.5 * math.sqrt(x * x + y * y)

    def paint_angle(self, painter):
        x1, y1 = self.pos_src
        x2, y2 = self.pos_dst
        length = self.get_distance(self.edge.end_item.boundingRect().width(), self.edge.end_item.boundingRect().height())  # 圆点距离终点图元的距离
        k = math.atan2(y2 - y1, x2 - x1)  # theta
        new_x = x2 - length * math.cos(k)  # 减去线条自身的宽度
        new_y = y2 - length * math.sin(k)
        new_x1 = new_x - 20 * math.cos(k - np.pi / 8)
        new_y1 = new_y - 20 * math.sin(k - np.pi / 8)
        new_x2 = new_x - 20 * math.cos(k + np.pi / 8)
        new_y2 = new_y - 20 * math.sin(k + np.pi / 8)
        painter.setPen(self._pen)
        painter.setBrush(self._mark_brush)
        point1 = QPoint(int(new_x), int(new_y))
        point2 = QPoint(int(new_x1), int(new_y1))
        point3 = QPoint(int(new_x2), int(new_y2))
        line1 = QLine(point1,point2)
        line2 = QLine(point1,point3)
        painter.drawLine(line1)
        painter.drawLine(line2)

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
            self.paint_angle(painter)
