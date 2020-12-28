# Inspired by PyQt5 Creating Paint Application In 40 Minutes
#  https://www.youtube.com/watch?v=qEgyGyVA1ZQ

# PyQt documentation links are prefixed with the word 'documentation' in the code below and can be accessed automatically
#  in PyCharm using the following technique https://www.jetbrains.com/help/pycharm/inline-documentation.html

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QMessageBox, QColorDialog, QDialog, \
    QTextEdit, QGridLayout, QWidget, QGroupBox, QSlider, QLabel, QVBoxLayout, QRadioButton, QPushButton
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QSize

import platform
import sys

from src.Painter import Painter
from src.Tools import Tools


class PaintingApplication(QMainWindow):  # documentation https://doc.qt.io/qt-5/qmainwindow.html
    """Painting Application class"""

    def __init__(self):
        super().__init__()

        # join style components
        self.bevelJoinBtn = QRadioButton("Bevel")
        self.roundJoinBtn = QRadioButton("Round")
        self.miterJoinBtn = QRadioButton("Miter")
        self.penJoinStyle = QGroupBox("Brush Join Style")

        # brush width components
        self.brushWidthLabel = QLabel()
        self.brushWidth = QSlider(Qt.Horizontal)
        self.groupBoxSlider = QGroupBox("Brush Width")

        # brush cap style components
        self.brushCapStyle = QGroupBox("Brush Cap Style")
        self.flatCapBtn = QRadioButton("Flat")
        self.roundCapBtn = QRadioButton("Round")
        self.squareCapBtn = QRadioButton("Square")

        # brush line style components
        self.dotLineBtn = QRadioButton("Dot")
        self.dashLineBtn = QRadioButton("Dash")
        self.solidLineBtn = QRadioButton("Solid")
        self.brushLineType = QGroupBox("Brush Line Style")

        # brush color components
        self.brushColorPushBtn = QPushButton()
        self.brushColor = QColor(0, 0, 255) # blue color
        self.groupBoxColor = QGroupBox("Brush Color")

        # set the main window title
        self.setWindowTitle("Paint Application")

        # set the main window location and dimension
        top, left, width, height = 350, 50, 700, 500
        self.setGeometry(top, left, width, height)

        # set the icon
        # windows version
        self.setWindowIcon(QIcon("icons/paint-brush.png")) # documentation: https://doc.qt.io/qt-5/qwidget.html#windowIcon-prop
        # mac version - not yet working
        # self.setWindowIcon(QIcon(QPixmap("./icons/paint-brush.png")))

        # init the main layout with a painting and tools area
        self.grid = QGridLayout()
        self.tools = Tools()
        self.painter = Painter()

        # init layouts for the required brush painting tools
        self.initBrushCapStyle()
        self.initBrushJoinStyle()
        self.initBrushLineStyle()
        self.initBrushWidth()
        self.initBrushColor()

        self.grid.addWidget(self.painter, 0, 0)
        self.grid.addWidget(self.tools, 0, 1)
        mainWindow = QWidget()
        mainWindow.setLayout(self.grid)
        self.setCentralWidget(mainWindow)

        # init menus
        mainMenu = self.menuBar()  # create and a menu bar
        # it is needed for MacOS, see https://stackoverflow.com/a/31028590
        if platform.system().lower() == "darwin":
            mainMenu.setNativeMenuBar(False)

        fileMenu = mainMenu.addMenu(" File") # add the file menu to the menu bar, the space is required as "File" is reserved in Mac
        brushSizeMenu = mainMenu.addMenu(" Brush Size") # add the "Brush Size" menu to the menu bar
        brushColorMenu = mainMenu.addMenu(" Brush Color") # add the "Brush Color" menu to the menu bar
        helpMenu = mainMenu.addMenu(" Help ") # add the "Help" menu to the menu bar

        # open menu item
        openAction = QAction(QIcon("icons/open.png"), "Open", self)   # create a open action with a png as an icon, documenation: https://doc.qt.io/qt-5/qaction.html
        openAction.setShortcut("Ctrl+O")                              # connect this save action to a keyboard shortcut, documentation: https://doc.qt.io/qt-5/qaction.html#shortcut-prop
        fileMenu.addAction(openAction)                                # add the save action to the file menu, documentation: https://doc.qt.io/qt-5/qwidget.html#addAction
        openAction.triggered.connect(self.open)                       # when the menu option is selected or the shortcut is used the save slot is triggered, documenation: https://doc.qt.io/qt-5/qaction.html#triggered


        # save menu item
        saveAction = QAction(QIcon("icons/save.png"), "Save", self)   # create a save action with a png as an icon, documenation: https://doc.qt.io/qt-5/qaction.html
        saveAction.setShortcut("Ctrl+S")                                # connect this save action to a keyboard shortcut, documentation: https://doc.qt.io/qt-5/qaction.html#shortcut-prop
        fileMenu.addAction(saveAction)                                  # add the save action to the file menu, documentation: https://doc.qt.io/qt-5/qwidget.html#addAction
        saveAction.triggered.connect(self.save)                         # when the menu option is selected or the shortcut is used the save slot is triggered, documenation: https://doc.qt.io/qt-5/qaction.html#triggered

        # clear
        clearAction = QAction(QIcon("icons/clear.png"), "Clear", self) # create a clear action with a png as an icon
        clearAction.setShortcut("Ctrl+C")                                # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)                                  # add this action to the file menu
        clearAction.triggered.connect(self.clear)                        # when the menu option is selected or the shortcut is used the clear slot is triggered

        # exit
        exitAction = QAction(QIcon('icons/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exit)
        fileMenu.addAction(exitAction)

        # brush thickness
        threepxAction = QAction(QIcon("../icons/threepx.png"), "3px", self)
        threepxAction.setShortcut("Ctrl+3")
        brushSizeMenu.addAction(threepxAction) # connect the action to the function below
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon("../icons/fivepx.png"), "5px", self)
        fivepxAction.setShortcut("Ctrl+5")
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon("../icons/sevenpx.png"), "7px", self)
        sevenpxAction.setShortcut("Ctrl+7")
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon("../icons/ninepx.png"), "9px", self)
        ninepxAction.setShortcut("Ctrl+9")
        brushSizeMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)

        # brush colors
        blackAction = QAction(QIcon("icons/black.png"), "Black", self)
        blackAction.setShortcut("Ctrl+B")
        brushColorMenu.addAction(blackAction);
        blackAction.triggered.connect(self.black)

        redAction = QAction(QIcon("icons/red.png"), "Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColorMenu.addAction(redAction);
        redAction.triggered.connect(self.red)

        greenAction = QAction(QIcon("icons/green.png"), "Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColorMenu.addAction(greenAction)
        greenAction.triggered.connect(self.green)

        yellowAction = QAction(QIcon("icons/yellow.png"), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColorMenu.addAction(yellowAction);
        yellowAction.triggered.connect(self.yellow)

        helpAction = QAction(QIcon("../icons/help.png"), "User Guide", self)
        helpAction.setShortcut("Ctrl+H")
        helpMenu.addAction(helpAction)
        helpAction.triggered.connect(self.help)

        aboutAction = QAction(QIcon("../icons/about.png"), "About", self)
        aboutAction.setShortcut("Ctrl+A")
        helpMenu.addAction(aboutAction)
        aboutAction.triggered.connect(self.about)

    # resize event - this function is called
    def resizeEvent(self, event):
        """Invoked when the window is resized"""
        if self.painter.resizeSavedImage.width() != 0:
            self.painter.image = self.painter.resizeSavedImage.scaled(self.painter.width(), self.painter.height(), Qt.IgnoreAspectRatio)
        self.painter.update()

    def brushWidthSliderChange(self, value):
        """Sets the pen size when the slider value changes"""
        self.painter.brushWidth = value
        self.brushWidthLabel.setText("{} px".format(value))

    def initBrushWidth(self):
        """Creates a QSlider that can be used to change the pen width"""
        self.groupBoxSlider.setMaximumHeight(100)

        self.brushWidth.setMinimum(1)
        self.brushWidth.setMaximum(25)
        self.brushWidth.valueChanged.connect(self.brushWidthSliderChange)

        self.brushWidthLabel.setText("{} px".format(self.painter.brushWidth))

        qv = QVBoxLayout()  # Add the slider and labels into a vbox
        qv.addWidget(self.brushWidth)
        qv.addWidget(self.brushWidthLabel)
        self.groupBoxSlider.setLayout(qv)

        self.tools.vbox.addWidget(self.groupBoxSlider)

    def initBrushLineStyle(self):
        """Init brush line styles"""
        self.brushLineType.setMaximumHeight(100)

        """
        Creates the radio buttons to let us make a choice between these 3 options.
        Each one is connected to a method which will change the setting depending on which
        button is clicked.
        """
        self.solidLineBtn.setIcon(QIcon("../icons/solid.png"))
        self.solidLineBtn.setIconSize(QSize(25, 50))
        self.solidLineBtn.clicked.connect(lambda: self.setBrushLineStyle(self.solidLineBtn))

        self.dashLineBtn.setIcon(QIcon("../icons/dash.png"))
        self.dashLineBtn.setIconSize(QSize(25, 50))
        self.dashLineBtn.clicked.connect(lambda: self.setBrushLineStyle(self.dashLineBtn))

        self.dotLineBtn.setIcon(QIcon("../icons/dot.png"))
        self.dotLineBtn.setIconSize(QSize(25, 50))
        self.dotLineBtn.clicked.connect(lambda: self.setBrushLineStyle(self.dotLineBtn))

        self.solidLineBtn.setChecked(True)  # the line is solid by default

        qv = QVBoxLayout()  # add all buttons onto a vbox
        qv.addWidget(self.solidLineBtn)
        qv.addWidget(self.dashLineBtn)
        qv.addWidget(self.dotLineBtn)

        self.brushLineType.setLayout(qv)
        self.tools.vbox.addWidget(self.brushLineType)

    def initBrushCapStyle(self):
        """makes it possible to select cap style from a QRadioButton"""
        self.brushCapStyle.setMaximumHeight(100)

        self.flatCapBtn.clicked.connect(lambda: self.setBrushCap(self.flatCapBtn))
        self.squareCapBtn.clicked.connect(lambda: self.setBrushCap(self.squareCapBtn))
        self.roundCapBtn.clicked.connect(lambda: self.setBrushCap(self.roundCapBtn))

        self.flatCapBtn.setChecked(True)  # flat cap is the default
        qv = QVBoxLayout()
        qv.addWidget(self.flatCapBtn)
        qv.addWidget(self.roundCapBtn)
        qv.addWidget(self.squareCapBtn)
        self.brushCapStyle.setLayout(qv)
        self.tools.vbox.addWidget(self.brushCapStyle)

    def initBrushJoinStyle(self):
        """Init join style that will be used by the pen"""
        self.penJoinStyle.setMaximumHeight(100)

        self.bevelJoinBtn.clicked.connect(lambda: self.setBrushJoin(self.bevelJoinBtn))
        self.miterJoinBtn.clicked.connect(lambda: self.setBrushJoin(self.miterJoinBtn))
        self.roundJoinBtn.clicked.connect(lambda: self.setBrushJoin(self.roundJoinBtn))

        self.bevelJoinBtn.setChecked(True)
        qv = QVBoxLayout()
        qv.addWidget(self.bevelJoinBtn)
        qv.addWidget(self.miterJoinBtn)
        qv.addWidget(self.roundJoinBtn)
        self.penJoinStyle.setLayout(qv)
        self.tools.vbox.addWidget(self.penJoinStyle)

    def initBrushColor(self):
        """Init components used to select and set brush color"""
        self.groupBoxColor.setMaximumHeight(100)

        self.brushColorPushBtn.setFixedSize(50, 50)
        self.brushColorPushBtn.clicked.connect(self.colorDialog)
        self.brushColorPushBtn.setStyleSheet("background-color: {}".format(self.brushColor.name()))
        self.tools.vbox.addWidget(self.brushColorPushBtn)

        # use vertical box layout
        qv = QVBoxLayout()
        qv.addWidget(self.brushColorPushBtn)
        self.groupBoxColor.setLayout(qv)

        self.tools.vbox.addWidget(self.groupBoxColor)

    def setBrushCap(self, btn):
        """Sets the brush cap based on the btn text"""
        if btn.text() == "Flat" and btn.isChecked():
            print("setting flat cap")
            self.painter.brushCap = Qt.FlatCap
        if btn.text() == "Round" and btn.isChecked():
            print("setting round cap")
            self.painter.brushCap = Qt.RoundCap
        if btn.text() == "Square" and btn.isChecked():
            print("setting square cap")
            self.painter.brushCap = Qt.SquareCap

    def setBrushJoin(self, btn):
        """Sets the brush join based on the btn text"""
        if btn.text() == "Bevel" and btn.isChecked():
            print("setting bevel join")
            self.painter.brushJoin = Qt.BevelJoin
        if btn.text() == "Miter" and btn.isChecked():
            print("setting miter join")
            self.painter.brushJoin = Qt.MiterJoin
        if btn.text() == "Round" and btn.isChecked():
            print("setting round join")
            self.painter.brushJoin = Qt.RoundJoin

    def setBrushLineStyle(self, btn):
        """Sets the brush line style based on the btn text"""
        if btn.text() == "Dash" and btn.isChecked():
            print("dash line style")
            self.painter.brushStyle = Qt.DashLine
        if btn.text() == "Dot" and btn.isChecked():
            print("dot line style")
            self.painter.brushStyle = Qt.DotLine
        if btn.text() == "Solid" and btn.isChecked():
            print("solid line style")
            self.painter.brushStyle = Qt.SolidLine

    def colorDialog(self):
        """Opens a QColorDialog to set the brush color"""
        self.brushColor = QColorDialog.getColor()
        if self.brushColor.isValid():
            self.brushColorPushBtn.setStyleSheet("background-color: {}".format(self.brushColor.name()))
            self.painter.brushColor = self.brushColor

    def save(self):
        """Saves the painting into an image"""
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if the file path is empty
            return  # do nothing and return
        self.painter.image.save(filePath)  # save file image to the file path

    def clear(self):
        """Clears the painting without saving it"""
        btnReply = QMessageBox.question(self, 'Clear Confirmation', "Clear Painting?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if btnReply == QMessageBox.Yes:
            self.painter.image.fill(Qt.white)   # fill the image with white, documentaiton: https://doc.qt.io/qt-5/qimage.html#fill-2
            self.painter.update()               # call the update method of the widget which calls the paintEvent of this class

    def threepx(self):
        """sets the brush width is set to 3"""
        self.painter.brushWidth = 3

    def fivepx(self):
        """sets the brush width is set to 5"""
        self.painter.brushWidth = 5

    def sevenpx(self):
        """sets the brush width is set to 7"""
        self.painter.brushWidth = 7

    def ninepx(self):
        """sets the brush width is set to 7"""
        self.painter.brushWidth = 9

    def black(self):
        """sets the brush color to black"""
        self.painter.brushColor = Qt.black

    def red(self):
        """sets the brush color to red"""
        self.painter.brushColor = Qt.red

    def green(self):
        """sets the brush color to green"""
        self.painter.brushColor = Qt.green

    def yellow(self):
        """sets the brush color to yellow"""
        self.painter.brushColor = Qt.yellow

    def help(self):
        """Opens a QDialog to display user guide and about pages under Help menu"""
        helpWindow = QDialog(self)
        tb = QTextEdit(helpWindow)
        tb.resize(350, 250)
        tb.setReadOnly(True)
        tb.setText("<p>User Guide</p>"
                   "<p>Menus:</p>"
                   "<p>File:<ul><li>Save</li><li>Clear</li><li>Exit</li></ul></p>"
                   "<p>Brush Size:<ul><li>3px</li><li>5px</li><li>7px</li><li>9px</li></ul></p>"
                   "<p>Brush Color:<ul><li>Black</li><li>Red</li><li>Green</li><li>Yellow</li></ul></p>"
                   "<p>Tools:</p>"
                   "<ul>"
                   "<li>Brush Cap Style</li>"
                   "<li>Brush Join Style</li>"
                   "<li>Brush Line Style</li>"
                   "<li>Brush Width</li>"
                   "<li>Brush Color</li>"
                   "</ul>"
                   )
        tb.setAlignment(Qt.AlignLeft)
        helpWindow.setWindowTitle("Help")
        helpWindow.setFixedHeight(260)
        helpWindow.setFixedWidth(360)
        helpWindow.show()

    def about(self):
        """Opens a QDialog to display about page"""
        aboutWindow = QDialog(self)
        tb = QTextEdit(aboutWindow)
        tb.resize(120, 120)
        tb.setReadOnly(True)
        tb.setText("<p>PyQt Paint</p>"
                   "<p>Version 1.0.0</p>")
        tb.setAlignment(Qt.AlignLeft)
        aboutWindow.setWindowTitle("About")
        aboutWindow.setFixedHeight(120)
        aboutWindow.setFixedWidth(120)
        aboutWindow.show()

    def open(self):
        """Opens a file dialog box and sets the QImage into the scaled version of the file"""
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":
            # if no file is selected return
            return

        # opens the file to read in binary mode
        with open(filePath, 'rb') as f:
            fileData = f.read()

        # loads file into the painter image variable
        self.painter.image.loadFromData(fileData)

        # gets the width of the current painter QImage
        width = self.width()
        # gets the height of the current painter QImage
        height = self.height()

        # scales the painter image from the file and put it in the QImage
        self.painter.image = self.painter.image.scaled(width, height)

        # update the widget
        self.update()

    def exit(self):
        """Exits the applications after a confirmation"""
        btnReply = QMessageBox.question(self, 'Exit Confirmation', "Exit Paint?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if btnReply == QMessageBox.Yes:
            self.close()


# this code will be executed if it is the main module but not if the module is imported
#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaintingApplication()
    window.show()
    # starts the event loop running
    app.exec()