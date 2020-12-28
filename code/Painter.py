from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint

class Painter(QWidget):
    def __init__(self):
        super().__init__()

        # set the windows dimensions
        top, left, width, height = 400, 400, 600, 400
        self.setGeometry(top, left, width, height)

        # set window icon
        self.setWindowIcon(QIcon("icons/paint-brush.png"))  # see: https://doc.qt.io/qt-5/qwidget.html#windowIcon-prop

        # default image settings
        self.image = QImage(self.size(), QImage.Format_RGB32)  # see: https://doc.qt.io/qt-5/qimage.html#QImage-1
        self.image.fill(Qt.white)  # see: https://doc.qt.io/qt-5/qimage.html#fill-1

        self.resizeSavedImage = QImage(0, 0, QImage.Format_RGB32)  # used for resizing of an opened image

        # set default values
        self.drawing = False
        self.brushColor = Qt.blue
        self.brushStyle = Qt.SolidLine
        self.brushCap = Qt.FlatCap
        self.brushJoin = Qt.MiterJoin
        self.brushWidth = 2

        # reference to last point recorded by mouse
        self.lastPoint = QPoint()  # see: https://doc.qt.io/qt-5/qpoint.html

    def mousePressEvent(self, event):
        """Mouse event handler that is called when mouse is pressed"""
        if event.button() == Qt.LeftButton:
            painter = QPainter(self.image)  # object which allows drawing to take place on an image
            painter.setPen(QPen(self.brushColor, self.brushWidth, self.brushStyle, self.brushCap, self.brushJoin))
            painter.drawPoint(event.pos())
            self.drawing = True  # set the drawing mode
            self.lastPoint = event.pos()  # save the last point

            self.update()  # update and render the new painting

    def mouseMoveEvent(self, event):
        """Mouse event handler that is called when mouse is moved"""
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brush width, line type, cap type, join type
            painter.setPen(QPen(self.brushColor, self.brushWidth, self.brushStyle, self.brushCap, self.brushJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """Mouse event handler that is called when mouse is released"""
        if event.button == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        """triggered by QPainter"""
        canvasPainter = QPainter(self)  # see https://doc.qt.io/qt-5/qpainter.html
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())  # draw the image , documentation: https://doc.qt.io/qt-5/qpainter.html#drawImage-1

    # resize event - this function is called
    def resizeEvent(self, event):
        """triggered when the painter is resized"""
        self.image = self.image.scaled(self.width(), self.height())