"""
Tools class inherited from a QWidget to init a tools panels on the painting panel of the app.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class Tools(QWidget):
    def __init__(self):
        super().__init__()

        self.setMaximumWidth(200)  # set the max width of the tool panel
        self.setMinimumWidth(200)  # set the min width of the tool panel

        self.vbox = QVBoxLayout()  # use vertical box as the layout
        self.setLayout(self.vbox)
