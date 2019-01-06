import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QImage
from PyQt5.QtCore import *


class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))


    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(QtCore.QPoint(event.pos()))
        super(PhotoViewer, self).mousePressEvent(event)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = PhotoViewer(self)


        # 'Load image' button 1
        self.btnLoad = QtWidgets.QToolButton(self)
        self.btnLoad.setText('Load image 1')
        self.btnLoad.clicked.connect(self.loadImage)
        # 'Load image' button 2
        self.btnLoad2 = QtWidgets.QToolButton(self)
        self.btnLoad2.setText('Load image 2')
        self.btnLoad2.clicked.connect(self.loadImage2)
        # Button close screen
        self.btnKon = QtWidgets.QPushButton(self)
        self.btnKon.setText('Zamknij')
        self.btnKon.clicked.connect(self.koniec)
        # Icon in left corner
        self.setWindowIcon(QIcon('mapa.jpg'))


        # Arrange layout
        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)
        HBlayout = QtWidgets.QHBoxLayout()
        #HBlayout.setAlignment(QtCore.Qt.AlignLeft)
        HBlayout.addWidget(self.btnLoad)
        HBlayout.addWidget(self.btnLoad2)
        HBlayout.addWidget(self.btnKon)
        VBlayout.addLayout(HBlayout)
        #self.showFullScreen()


    def loadImage(self):
        #self.showFullScreen()
        self.viewer.setPhoto(QtGui.QPixmap('orto.jpg'))

    def loadImage2(self):
        #self.showFullScreen()
        self.viewer.setPhoto(QtGui.QPixmap('orto2.JPG'))

    def pixInfo(self):
        self.viewer.toggleDragMode()

    def closeEvent(self, event):

        odp = QMessageBox.question(self, 'Komunikat', "Czy na pewno koniec?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def koniec(self):
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    #window.setGeometry(500, 300, 800, 600)
    window.showFullScreen()
    window.show()
    sys.exit(app.exec_())