# -*-coding = utf-8 -*-
# @Time : 2024/6/13 15:01
# @Author :skq
# @File : roll.py
# @Software: PyCharm
from PyQt5 import QtWidgets


def setroll():
    textEdit_send_sbar = QtWidgets.QScrollBar()

    # 2.给这个滚动条添加属性
    textEdit_send_sbar.setStyleSheet("""
         QScrollBar:vertical {
              border-width: 0px;
              border: none;
              background:rgba(64, 65, 79, 0);
              width:12px;
              margin: 0px 0px 0px 0px;
          }
          QScrollBar::handle:vertical {
              background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
              stop: 0 #8dcef9, stop: 0.5 #8dcef9, stop:1 #8dcef9);
              min-height: 20px;
              max-height: 20px;
              margin: 0 0px 0 0px;
              border-radius: 6px;
          }
          QScrollBar::add-line:vertical {
              background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
              stop: 0 rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
              height: 0px;
              border: none;
              subcontrol-position: bottom;
              subcontrol-origin: margin;
          }
          QScrollBar::sub-line:vertical {
              background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
              stop: 0  rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
              height: 0 px;
              border: none;
              subcontrol-position: top;
              subcontrol-origin: margin;
          }
          QScrollBar::sub-page:vertical {
          background: rgba(64, 65, 79, 0);
          }

          QScrollBar::add-page:vertical {
          background: rgba(64, 65, 79, 0);
          }
          
          
          
          
          
          QScrollBar:horizontal {
              border-height: 0px;
              border: none;
              background:rgba(64, 65, 79, 0);
              height:12px;
              margin: 0px 0px 0px 0px;
          }
          QScrollBar::handle:horizontal {
              background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
              stop: 0 #8dcef9, stop: 0.5 #8dcef9, stop:1 #8dcef9);
              min-width: 20px;
              max-width: 20px;
              margin: 0 0px 0 0px;
              border-radius: 6px;
          }
          QScrollBar::add-line:horizontal {
              background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
              stop: 0 rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
              width: 0px;
              border: none;
              subcontrol-position: bottom;
              subcontrol-origin: margin;
          }
          QScrollBar::sub-line:horizontal {
              background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
              stop: 0  rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
              width: 0 px;
              border: none;
              subcontrol-position: top;
              subcontrol-origin: margin;
          }
          QScrollBar::sub-page:horizontal {
          background: rgba(64, 65, 79, 0);
          }

          QScrollBar::add-page:horizontal {
          background: rgba(64, 65, 79, 0);
          }
          """)

    # 3.把这个textEdit_send_sbar当作属性附加到textEdit控件上
    return textEdit_send_sbar