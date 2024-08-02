import os
import sys
import time

import pptx.slide
import typing

from PyQt5 import QtGui
from PyQt5.QtCore import QUrl, Qt, QSize
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QScrollArea, QSlider, QFileDialog, \
    QHBoxLayout, QFrame
from PyQt5.QtGui import QPixmap, QImage, QWheelEvent, QResizeEvent
from pptx import Presentation
import fitz  # PyMuPDF
import comtypes.client



class PDFScrollArea(QScrollArea):
    def __init__(self, path):
        super().__init__()
        self.scale_factor = 1.0
        self.pdf_document = fitz.open(path)
        self.initUI()

    def initUI(self):
        self.pdf_widget = QWidget()
        self.pdf_layout = QVBoxLayout()
        self.pdf_widget.setLayout(self.pdf_layout)
        for page_num in range(len(self.pdf_document)):
            page = self.pdf_document.loadPage(page_num)
            pix = page.getPixmap(alpha=False)
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)

            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.setScaledContents(True)
            label.setPixmap(QPixmap.fromImage(img))
            label.setObjectName(f"page_{page_num}")

            h_layout = QHBoxLayout()
            h_layout.addStretch(1)
            h_layout.addWidget(label)
            h_layout.addStretch(1)

            self.pdf_layout.addLayout(h_layout)

        self.setWidget(self.pdf_widget)
        self.setWidgetResizable(True)
        self.resize(900, 1600)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0 and self.scale_factor < 5:
            self.scale_factor *= 1.1
        elif event.angleDelta().y() < 0 and self.scale_factor > 0.7:
            self.scale_factor *= 0.9

        self.update_images()

    def update_images(self):
        for i in range(len(self.pdf_document)):
            page = self.pdf_document.loadPage(i)
            pix = page.getPixmap(matrix=fitz.Matrix(self.scale_factor, self.scale_factor))
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)

            label = self.findChild(QLabel, f"page_{i}")
            if label:
                label.setPixmap(QPixmap.fromImage(img))


def createPDFWidget(path):
    return PDFScrollArea(path)


class ClickableSlider(QSlider):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            value = self.minimum() + (self.maximum() - self.minimum()) * pos.x() / self.width()
            self.setValue(int(value))
            self.sliderMoved.emit(int(value))
        super().mousePressEvent(event)


class VideoPlayer(QWidget):
    def __init__(self, path, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 900, 600)

        self.videoWidget = QVideoWidget()
        self.videoWidget.setFocusPolicy(Qt.StrongFocus)

        container_width = 900
        video_height = int(container_width * 9 / 16)

        self.videoWidget.setMinimumSize(container_width, video_height)
        self.videoWidget.setMaximumSize(container_width * 10, video_height * 10)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.videoWidget)

        self.controlLayout = QHBoxLayout()
        self.playPauseButton = QPushButton("Play/Pause")
        self.fullscreenButton = QPushButton("Fullscreen")
        self.controlLayout.addWidget(self.playPauseButton)
        self.controlLayout.addWidget(self.fullscreenButton)
        self.layout.addLayout(self.controlLayout)

        self.progressBar = ClickableSlider(Qt.Horizontal)
        self.progressBar.setRange(0, 1000)
        self.layout.addWidget(self.progressBar)

        self.setLayout(self.layout)

        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.videoWidget)
        self.player.setNotifyInterval(100)

        self.player.positionChanged.connect(self.updateProgressBar)
        self.player.durationChanged.connect(self.updateProgressBarRange)
        self.progressBar.sliderMoved.connect(self.setPlayerPosition)
        self.progressBar.sliderPressed.connect(lambda: self.player.setPosition(self.progressBar.sliderPosition()))
        self.progressBar.sliderReleased.connect(lambda: self.player.setPosition(self.progressBar.sliderPosition()))
        self.is_fullscreen = False
        self.media = QMediaContent(QUrl.fromLocalFile(path))
        self.player.setMedia(self.media)

        self.playPauseButton.clicked.connect(self.togglePlayPause)
        self.fullscreenButton.clicked.connect(self.toggleFullscreen)

    def keyPressEvent(self, a0: typing.Optional[QtGui.QKeyEvent]) -> None:
        print(a0.text().encode())
        if a0.key() == Qt.Key_Escape:
            self.toggleFullscreen()

    def updateProgressBar(self, pos):
        self.progressBar.setValue(pos)

    def updateProgressBarRange(self, dur):
        self.progressBar.setRange(0, dur)

    def setPlayerPosition(self, pos):
        self.player.setPosition(pos)

    def togglePlayPause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def toggleFullscreen(self):
        if not self.is_fullscreen:
            self.showFullScreen()
        else:
            self.showNormal()
        self.is_fullscreen = not self.is_fullscreen


def delete_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"成功删除文件: {file_path}")


def ppt_to_images(ppt_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    delete_files(output_folder)
    # Initialize the PowerPoint application
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = 1

    # Open the presentation
    presentation = powerpoint.Presentations.Open(ppt_path)

    # Save each slide as an image
    for i, slide in enumerate(presentation.Slides):
        print(i,slide)
        image_path = os.path.join(output_folder, f"slide_{i + 1}.jpg")
        slide.Export(image_path, "JPG")

    # Close the presentation and quit PowerPoint
    presentation.Close()
    powerpoint.Quit()



def slide_to_image(im_path, ppt_path):
    # Create a blank image with white background
    try:
        # Create a directory to store images named after the PPT file
            # Initialize COM for PowerPoint
        #delete_files(im_path)
        ppt_to_images(ppt_path, im_path)

    # Display the images

    except Exception as e:
        print(f"Error displaying PPT: {e}")


class PptWindow(QWidget):
    def __init__(self, ppt_path):
        super().__init__()
        self.scale_factor = 1.0  # Initial scale factor
        self.initUI(ppt_path)

    def initUI(self, ppt_path):
        self.ppt_widget = QWidget()
        self.ppt_layout = QVBoxLayout()
        self.ppt_widget.setLayout(self.ppt_layout)
        self.labels = []
        self.ppt_scroll = QScrollArea()
        self.ppt_scroll.setWidget(self.ppt_widget)
        self.ppt_scroll.setWidgetResizable(True)
        self.path = ppt_path
        filename = os.path.basename(ppt_path)
        container_width = self.width() - 40  # 减去一些边距
        self.img_dir = os.path.join(os.getcwd(), '.picture', filename)
        slide_to_image(im_path=self.img_dir, ppt_path=self.path)
        for img_file in sorted(os.listdir(self.img_dir)):
            if img_file.endswith('.jpg'):
                img_path = os.path.join(self.img_dir, img_file)
                img = QImage(img_path)

                pixmap = QPixmap.fromImage(img)
                scaled_pixmap = pixmap.scaledToWidth(container_width, Qt.SmoothTransformation)

                label = QLabel()
                label.setPixmap(scaled_pixmap)
                label.setAlignment(Qt.AlignCenter)
                label.setScaledContents(False)
                self.labels.append(label)
                h_layout = QHBoxLayout()
                h_layout.addStretch(1)
                h_layout.addWidget(label)
                h_layout.addStretch(1)

                self.ppt_layout.addLayout(h_layout)

        self.ppt_widget.adjustSize()

        ppt_container = QVBoxLayout()
        ppt_container.addWidget(self.ppt_scroll)

        self.setLayout(ppt_container)





        #
        # self.path = ppt_path
        # filename = os.path.basename(ppt_path)
        # layout = QVBoxLayout()
        # self.scroll_area = QScrollArea()
        # content_widget = QWidget()
        # self.ppt_layout = QVBoxLayout()
        # self.img_dir = os.path.join(os.getcwd(), '.picture', filename)
        # slide_to_image(im_path=self.img_dir, ppt_path=self.path)
        # self.labels = []
        #
        # for img_file in sorted(os.listdir(self.img_dir)):
        #     if img_file.endswith('.jpg'):
        #         img_path = os.path.join(self.img_dir, img_file)
        #         img = QImage(img_path)
        #
        #         pixmap = QPixmap.fromImage(img)
        #
        #
        #         label = QLabel()
        #         #
        #         # size = QSize()
        #         # size.setHeight(label.height())
        #         # size.setWidth(label.width())
        #         #
        #         # pixmap = pixmap.scaled(size, Qt.IgnoreAspectRatio)
        #         # #
        #         # pixmap.scaled(Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        #
        #         label.setAlignment(Qt.AlignCenter)
        #         label.setScaledContents(False)
        #         label.setPixmap(pixmap)
        #
        #         self.ppt_layout.addWidget(label)
        #         self.labels.append(label)
        #
        # content_widget.setLayout(self.ppt_layout)
        # self.scroll_area.setWidget(content_widget)
        # layout.addWidget(self.scroll_area)
        # self.setLayout(layout)
        # self.setWindowTitle('PPT Viewer')
        #
        #
        #
        #
        #


    def wheelEvent(self, event: QWheelEvent):
        # Determine the zoom direction
        if event.angleDelta().y() > 0:
            self.scale_factor *= 1.1  # Zoom in
        else:
            self.scale_factor /= 1.1  # Zoom out

        # Adjust the scaling factor within reasonable bounds
        self.scale_factor = min(max(self.scale_factor, 0.1), 3.0)

        self.resizeEvent(None)

    def resizeEvent(self, event: typing.Optional[QResizeEvent]):
        for label in self.labels:
            pixmap = label.pixmap()
            if pixmap:
                scaled_pixmap = pixmap.scaled(
                    self.size() * self.scale_factor,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                label.setPixmap(scaled_pixmap)
                label.resize(scaled_pixmap.size())

    def closeEvent(self, event: typing.Optional[QtGui.QCloseEvent]) -> None:
        delete_files(self.img_dir)
        super().closeEvent(event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.button = QPushButton('Open PPT')
        self.button.clicked.connect(self.show_ppt)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.setWindowTitle('Main Window')
        self.resize(300, 200)

    def show_ppt(self):
        self.ppt_window = PptWindow(r'C:\Users\86150\Desktop\学习文件\23S103137-宋克强-知识图谱-1~4.pptx')
        self.ppt_window.show()


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    main_win = MainWindow()
    # main_win = VideoPlayer(path=r'C:\Users\86150\Videos\Captures\result 2023-05-29 20-33-54.mp4')
    # main_win = VideoPlayer(path=r"C:\Users\86150\Videos\Captures\result 2023-05-29 20-33-54.mp4")
    #main_win = createPDFWidget(path=r'C:\Users\86150\Desktop\论文集合\1512.03385.pdf')
    main_win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
