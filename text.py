# -*-coding = utf-8 -*-
# @Time : 2024/7/20 16:57
# @Author :skq
# @File : text.py
# @Software: PyCharm
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

if __name__ == '__main__':
    app = QApplication([])
    player = QMediaPlayer()
    wgt_video = QVideoWidget()  # 视频显示的widget
    wgt_video.show()
    player.setVideoOutput(wgt_video)  # 视频输出的widget
    player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # 选取视频文件
    player.play()
    app.exec_()
